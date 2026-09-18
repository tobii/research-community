#!/usr/bin/env python3
"""
Head orientation (Euler angles) from a raw Tobii Pro Glasses 3 recording.

Reads the `imudata.gz` of a G3 recording folder and writes roll / pitch / yaw
plus angular velocity, using the same Madgwick AHRS pipeline Tobii runs
server-side. No cloud upload and no normalization step is needed — this reads
the on-glasses files directly.

    python g3_imu_euler.py <recording-folder>
    python g3_imu_euler.py <recording-folder> --out ./orientation

Requires: numpy, scipy, ahrs   (pip install numpy scipy ahrs)

Run with --help for the full option list, and see README.md for the file
format, the coordinate conventions, and the magnetometer caveat.
"""

from __future__ import annotations

import argparse
import gzip
import json
import math
import pathlib
import sys

import numpy as np
from ahrs.common.orientation import q2euler
from ahrs.filters import Madgwick
from scipy.interpolate import interp1d
from scipy.ndimage import uniform_filter1d

# ============================ Conventions ============================
#
# G3 head unit coordinate system (HUCS), right-handed:
#   X = Left,  Y = Up,  Z = Forward
#
# Confirmed empirically on the sample recording: at rest the accelerometer
# mean is ~[0.1, 9.1, -1.8] m/s^2, i.e. gravity on +Y, so Y is up.
#
# The Python `ahrs` Madgwick filter expects a right-handed FLU frame with
# gravity at rest on axis 2:
#   axis 0 = Forward, axis 1 = Left, axis 2 = Up
#
# HUCS -> AHRS is therefore (Z, X, Y): forward=HUCS Z, left=HUCS X, up=HUCS Y.
IMU_ORIENTATION = "ZXY"

# Madgwick filter gain. sqrt(3/4) * gyro_noise ~= 0.04 for consumer IMUs;
# this is the value Tobii's server-side pipeline uses for head tracking.
MADGWICK_BETA = 0.04

# Angular-velocity smoothing, in milliseconds of wall time.
#
# The server-side pipeline hard-codes 100 *samples*, which is ~250 ms at the
# Glasses X rate of ~400 Hz. G3 samples at ~118 Hz, where 100 samples would be
# ~850 ms — a very different filter. Expressing the window in milliseconds and
# converting with the measured rate keeps the smoothing equivalent across both
# devices; pass --smooth-ms to change it.
SMOOTH_MS = 250.0

# Earth's magnetic field strength, for the sanity check on the magnetometer.
EARTH_FIELD_MIN_UT = 25.0
EARTH_FIELD_MAX_UT = 65.0


# ============================ Raw G3 loading ============================


def open_maybe_gzipped(path: pathlib.Path):
    """
    Open the IMU file as text, whether or not it is still gzipped.

    The glasses write `imudata.gz` compressed, but people decompress it to look
    inside and then pass that, so accept both rather than failing on a detail.
    """
    try:
        with gzip.open(path, mode="rb") as probe:
            probe.read(1)
    except gzip.BadGzipFile:
        return open(path)
    except OSError as exc:
        raise SystemExit(f"cannot read {path}: {exc}") from exc
    return gzip.open(path, mode="rt")


def load_g3_imu(path: pathlib.Path) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    """
    Parse a raw G3 `imudata.gz`.

    The file is gzipped newline-delimited JSON. Every line is one sample of one
    sensor, and the sensors are interleaved rather than aligned: accelerometer
    and gyroscope share a timestamp and arrive together at ~118 Hz, while the
    magnetometer arrives separately at ~10 Hz.

        {"type":"imu","timestamp":0.005992,"data":{
            "accelerometer":[-0.250,9.689,-1.427],
            "gyroscope":[-1.294,-0.345,1.037]}}
        {"type":"imu","timestamp":0.067795,"data":{
            "magnetometer":[300.199,-339.889,167.661]}}

    A line may therefore carry accelerometer+gyroscope, or magnetometer, and a
    reader must not assume every line has every field.

    Units as written by the glasses: accelerometer m/s^2, gyroscope
    **degrees/s**, magnetometer microtesla. The gyroscope is converted to
    radians/s here, which is what the filter and the Tobii cloud format use.

    Returns a dict of sensor name -> (times, (N, 3) vectors).
    """
    acc_t: list[float] = []
    acc_v: list[list[float]] = []
    gyr_t: list[float] = []
    gyr_v: list[list[float]] = []
    mag_t: list[float] = []
    mag_v: list[list[float]] = []

    with open_maybe_gzipped(path) as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(
                    f"{path}:{line_number}: not valid JSON ({exc}). "
                    "Is this really a G3 imudata.gz?"
                ) from exc

            if not isinstance(item, dict) or "timestamp" not in item:
                raise SystemExit(
                    f"{path}:{line_number}: no 'timestamp' field. Expected one "
                    "IMU sample per line; is this really a G3 imudata.gz? "
                    "(recording.g3 and gazedata.gz are different files.)"
                )

            data = item.get("data") or {}
            timestamp = item["timestamp"]

            if "accelerometer" in data:
                acc_t.append(timestamp)
                acc_v.append(data["accelerometer"])
            if "gyroscope" in data:
                gyr_t.append(timestamp)
                # G3 writes degrees/s; the filter wants radians/s.
                gyr_v.append([math.radians(g) for g in data["gyroscope"]])
            if "magnetometer" in data:
                mag_t.append(timestamp)
                mag_v.append(data["magnetometer"])

    def pack(times: list[float], vectors: list[list[float]]) -> tuple:
        return (
            np.asarray(times, dtype=float),
            np.asarray(vectors, dtype=float).reshape(-1, 3),
        )

    return {
        "accelerometer": pack(acc_t, acc_v),
        "gyroscope": pack(gyr_t, gyr_v),
        "magnetometer": pack(mag_t, mag_v),
    }


def resolve_imu_path(target: pathlib.Path) -> pathlib.Path:
    """Accept either a recording folder or the imudata.gz itself."""
    if target.is_dir():
        candidate = target / "imudata.gz"
        if not candidate.exists():
            raise SystemExit(
                f"no imudata.gz in {target}. A G3 recording folder holds "
                "recording.g3, imudata.gz, gazedata.gz, scenevideo.mp4 and meta/."
            )
        return candidate
    if not target.exists():
        raise SystemExit(f"no such file or folder: {target}")
    return target


def read_recording_metadata(folder: pathlib.Path) -> dict:
    """Read recording.g3 next to the IMU file, if it is there. Optional."""
    manifest = folder / "recording.g3"
    if not manifest.exists():
        return {}
    try:
        with open(manifest) as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError):
        return {}


# ============================ Sensor preparation ============================


def apply_orientation(
    data: np.ndarray, orient_str: str = IMU_ORIENTATION
) -> np.ndarray:
    """
    Remap axes from HUCS to the frame the AHRS filter expects.

    Each character of *orient_str* selects a source column; uppercase keeps the
    sign, lowercase negates it. X -> col 0, Y -> col 1, Z -> col 2. The default
    "ZXY" maps HUCS [Left, Up, Forward] to AHRS [Forward, Left, Up].
    """
    columns = {"x": 0, "y": 1, "z": 2}

    def column(char: str) -> np.ndarray:
        index = columns[char.lower()]
        sign = 1.0 if char.isupper() else -1.0
        return sign * data[:, index]

    return np.column_stack([column(c) for c in orient_str])


def fit_hard_iron(mag: np.ndarray) -> tuple[np.ndarray, float, float]:
    """
    Least-squares sphere fit to estimate a constant magnetometer offset.

    A magnetometer reads m = h + R.b, where b is Earth's field (constant
    magnitude) and h is a fixed "hard iron" offset from magnetised material near
    the sensor. As the head rotates, R.b sweeps a sphere of radius |b| centred
    on h — so fitting a sphere recovers both.

    Expanding |m - h|^2 = r^2 gives 2.m.h + (r^2 - |h|^2) = |m|^2, which is
    linear in the four unknowns (h, r^2 - |h|^2).

    Returns (offset, radius, residual_std). A fit is only trustworthy when the
    recording actually rotates through a good part of the sphere; residual_std
    is the diagnostic for that, and the caller should report it.
    """
    design = np.hstack([2.0 * mag, np.ones((len(mag), 1))])
    target = (mag**2).sum(axis=1)
    solution, *_ = np.linalg.lstsq(design, target, rcond=None)
    offset = solution[:3]
    radius = float(np.sqrt(solution[3] + (offset**2).sum()))
    residual_std = float(np.linalg.norm(mag - offset, axis=1).std())
    return offset, radius, residual_std


def align_magnetometer(
    target_times: np.ndarray, mag_times: np.ndarray, mag: np.ndarray
) -> np.ndarray:
    """
    Interpolate the magnetometer onto the gyro/accel timeline.

    G3 samples the magnetometer ~12x slower than the gyroscope, so this
    upsamples it linearly. Values before the first and after the last
    magnetometer sample are extrapolated from the nearest segment.
    """
    interpolate = interp1d(
        mag_times,
        mag,
        axis=0,
        kind="linear",
        bounds_error=False,
        fill_value="extrapolate",
    )
    return interpolate(target_times)


# ============================ Orientation ============================


def run_madgwick(
    gyro: np.ndarray,
    acc: np.ndarray,
    mag: np.ndarray | None,
    rate_hz: float,
    beta: float = MADGWICK_BETA,
) -> np.ndarray:
    """
    Run the Madgwick filter over remapped samples and return (N, 4) quaternions.

    With *mag*, this is MARG: the magnetometer gives an absolute heading, so yaw
    is referenced to magnetic north and does not drift. Without it, the filter
    has only gravity to correct against, which observes roll and pitch but says
    nothing about yaw — so yaw becomes relative to the start of the recording
    and drifts with gyro bias.
    """
    if mag is None:
        return Madgwick(gyr=gyro, acc=acc, frequency=rate_hz, beta=beta).Q
    return Madgwick(gyr=gyro, acc=acc, mag=mag, frequency=rate_hz, beta=beta).Q


def quaternion_rotation_matrices(quaternions: np.ndarray) -> np.ndarray:
    """(N, 4) quaternions -> (N, 3, 3) body-to-world rotation matrices."""
    w, x, y, z = quaternions.T
    return np.stack(
        [
            np.stack(
                [1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)], -1
            ),
            np.stack(
                [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)], -1
            ),
            np.stack(
                [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)], -1
            ),
        ],
        -2,
    )


def tilt_error_vs_gravity(quaternions: np.ndarray, acc_remapped: np.ndarray) -> dict:
    """
    Measure how far the filter's attitude is from what gravity says.

    While the head is not accelerating, the accelerometer direction *is* the
    up-vector, so it can referee the filter. Rotating the filter's own idea of
    world-up into the body frame and taking the angle between the two gives a
    tilt error in degrees. It is independent of every Euler sign convention, and
    it is the only way to tell from the data alone whether the magnetometer is
    helping or hurting.

    Samples are restricted to those within 0.3 m/s^2 of 1 g, which excludes
    walking and head-turn transients where the accelerometer is not gravity.

    Returns {} if the recording has too few quiet samples to judge.
    """
    magnitude = np.linalg.norm(acc_remapped, axis=1)
    quiet = np.abs(magnitude - 9.81) < 0.3
    if quiet.sum() < 100:
        return {}

    up_in_body = quaternion_rotation_matrices(quaternions)[:, 2, :]
    measured_up = acc_remapped / magnitude[:, None]
    cosine = np.clip((up_in_body * measured_up).sum(axis=1), -1.0, 1.0)
    error = np.degrees(np.arccos(cosine))[quiet]
    return {
        "n_quiet": int(quiet.sum()),
        "n_total": int(len(quiet)),
        "mean": float(error.mean()),
        "median": float(np.median(error)),
        "p95": float(np.percentile(error, 95)),
    }


def quaternions_to_euler(quaternions: np.ndarray) -> np.ndarray:
    """
    Convert quaternions to Euler angles in degrees, in Tobii's sign convention.

    `q2euler` uses the aerospace ZYX convention, whose raw output is
        col 0 = roll,  positive = right ear down
        col 1 = pitch, positive = nose up
        col 2 = yaw,   positive = turning right

    Tobii's pipeline negates pitch and yaw so that positive means looking down
    and turning left, and unwraps yaw so it accumulates continuously instead of
    jumping at +/-180 degrees. Both are reproduced here so output matches the
    server-side stream.
    """
    euler = np.degrees(np.array([q2euler(q) for q in quaternions]))
    euler[:, 1] = -euler[:, 1]  # +ve = looking down
    euler[:, 2] = -euler[:, 2]  # +ve = turning left
    euler[:, 2] = np.unwrap(euler[:, 2], period=360.0)
    return euler


def angular_velocity(
    euler: np.ndarray, rate_hz: float, smooth_ms: float = SMOOTH_MS
) -> np.ndarray:
    """
    Differentiate Euler angles into degrees/second, with a moving-average
    smoothing window expressed in milliseconds (see SMOOTH_MS).
    """
    window = max(1, int(round(smooth_ms * 1e-3 * rate_hz)))
    delta = np.diff(euler, axis=0)
    delta = np.vstack([np.zeros((1, 3)), delta])
    return uniform_filter1d(delta, size=window, axis=0) * rate_hz


# ============================ Orchestration ============================


def prepare_magnetometer(
    gyro_times: np.ndarray,
    mag_times: np.ndarray,
    mag: np.ndarray,
    use_magnetometer: bool,
    hard_iron: str,
    report=print,
) -> tuple[np.ndarray | None, str]:
    """
    Decide what the filter gets for a magnetometer, and say so.

    Returns (remapped magnetometer aligned to gyro_times, or None to run
    gyro+accelerometer only; a one-line description of what was done).
    """
    if not use_magnetometer:
        return None, "not used (gyro + accelerometer only; yaw is relative and drifts)"

    if len(mag) == 0:
        report(
            "  warning: no magnetometer samples in this recording; "
            "falling back to gyro + accelerometer"
        )
        return None, "absent (gyro + accelerometer only; yaw is relative and drifts)"

    field = float(np.linalg.norm(mag, axis=1).mean())
    report(f"  magnetometer: {len(mag)} samples, mean |B| = {field:.1f} uT")

    if hard_iron == "auto":
        offset, radius, residual = fit_hard_iron(mag)
        report(
            f"  hard-iron fit: offset {np.round(offset, 1)} uT, "
            f"field {radius:.1f} uT, residual sigma {residual:.1f} uT"
        )
        if not EARTH_FIELD_MIN_UT <= radius <= EARTH_FIELD_MAX_UT:
            report(
                f"  warning: fitted field {radius:.1f} uT is outside Earth's "
                f"{EARTH_FIELD_MIN_UT:.0f}-{EARTH_FIELD_MAX_UT:.0f} uT range; "
                "the recording may not rotate enough to constrain the fit"
            )
        mag_corrected = mag - offset
        note = f"hard-iron corrected, offset {np.round(offset, 1).tolist()} uT"
    else:
        if not EARTH_FIELD_MIN_UT <= field <= EARTH_FIELD_MAX_UT:
            report(
                f"  WARNING: mean |B| = {field:.1f} uT is far outside Earth's "
                f"{EARTH_FIELD_MIN_UT:.0f}-{EARTH_FIELD_MAX_UT:.0f} uT range. "
                "The magnetometer is uncalibrated, and yaw will be wrong. "
                "Re-run with --check to compare modes, --hard-iron auto to "
                "remove a constant offset, or --no-mag to ignore it."
            )
        mag_corrected = mag
        note = "raw, uncalibrated"

    aligned = align_magnetometer(gyro_times, mag_times, mag_corrected)
    return apply_orientation(aligned), note


def compute_orientation(
    streams: dict[str, tuple[np.ndarray, np.ndarray]],
    use_magnetometer: bool = True,
    hard_iron: str = "none",
    smooth_ms: float = SMOOTH_MS,
    report=print,
) -> dict:
    """
    Raw G3 streams -> Euler angles and angular velocity.

    Mirrors Tobii's server-side pipeline: align the magnetometer onto the
    gyro/accel timeline, remap axes, Madgwick, Euler, smoothed derivative.
    """
    acc_times, acc = streams["accelerometer"]
    gyro_times, gyro = streams["gyroscope"]
    mag_times, mag = streams["magnetometer"]

    if len(gyro) == 0 or len(acc) == 0:
        raise SystemExit(
            "the recording has no gyroscope or accelerometer samples; "
            "orientation cannot be computed"
        )
    if len(acc_times) != len(gyro_times):
        raise SystemExit(
            f"accelerometer ({len(acc_times)}) and gyroscope ({len(gyro_times)}) "
            "sample counts differ; expected them to be co-timestamped"
        )

    # Drop non-positive timestamps. G3 recordings normally have none, but the
    # server-side pipeline filters them and some devices emit pre-roll samples.
    keep = gyro_times >= 0
    n_dropped = int((~keep).sum())
    if n_dropped:
        report(f"  dropped {n_dropped} sample(s) with negative timestamps")
    gyro_times = gyro_times[keep]
    gyro = gyro[keep]
    acc = acc[keep]

    intervals = np.diff(gyro_times)
    if len(intervals) == 0 or np.median(intervals) <= 0:
        raise SystemExit("cannot determine the IMU sample rate from timestamps")
    rate_hz = float(1.0 / np.median(intervals))

    report(f"  samples:     {len(gyro_times)}")
    report(f"  sample rate: {rate_hz:.2f} Hz")
    report(f"  duration:    {gyro_times[-1] - gyro_times[0]:.2f} s")

    mag_for_filter, mag_note = prepare_magnetometer(
        gyro_times, mag_times, mag, use_magnetometer, hard_iron, report
    )
    report(f"  magnetometer: {mag_note}")

    acc_remapped = apply_orientation(acc)
    quaternions = run_madgwick(
        apply_orientation(gyro),
        acc_remapped,
        mag_for_filter,
        rate_hz,
    )
    euler = quaternions_to_euler(quaternions)
    velocity = angular_velocity(euler, rate_hz, smooth_ms)

    tilt = tilt_error_vs_gravity(quaternions, acc_remapped)
    if tilt:
        report(
            f"  tilt error vs gravity: {tilt['mean']:.2f} deg mean "
            f"({tilt['median']:.2f} median) over {tilt['n_quiet']} "
            "low-acceleration samples"
        )
        if tilt["mean"] > 10.0:
            report(
                "  warning: that is a large disagreement with gravity. Run with "
                "--check to compare magnetometer modes on this recording."
            )

    return {
        "times": gyro_times,
        "euler": euler,
        "angular_velocity": velocity,
        "rate_hz": rate_hz,
        "magnetometer": mag_note,
        "tilt_error": tilt,
    }


# ============================ Output ============================


def compare_magnetometer_modes(
    streams: dict[str, tuple[np.ndarray, np.ndarray]],
) -> None:
    """
    Run all three magnetometer modes and score each against gravity.

    Whether the magnetometer helps is a property of the environment, not of the
    glasses: indoors, steel shelving and motors distort the local field, and a
    distorted field drags the filter's attitude away from gravity. That shows up
    here as a larger tilt error. Use the winner for the real run.
    """
    _, acc = streams["accelerometer"]
    gyro_times, gyro = streams["gyroscope"]
    mag_times, mag = streams["magnetometer"]

    keep = gyro_times >= 0
    gyro_times, gyro, acc = gyro_times[keep], gyro[keep], acc[keep]
    rate_hz = float(1.0 / np.median(np.diff(gyro_times)))
    gyro_remapped = apply_orientation(gyro)
    acc_remapped = apply_orientation(acc)

    candidates: list[tuple[str, np.ndarray | None]] = [("--no-mag", None)]
    if len(mag):
        candidates.append(
            (
                "default (raw mag)",
                apply_orientation(align_magnetometer(gyro_times, mag_times, mag)),
            )
        )
        offset, radius, residual = fit_hard_iron(mag)
        candidates.append(
            (
                "--hard-iron auto",
                apply_orientation(
                    align_magnetometer(gyro_times, mag_times, mag - offset)
                ),
            )
        )
        print(
            f"  hard-iron fit: offset {np.round(offset, 1)} uT, field {radius:.1f} uT, "
            f"residual sigma {residual:.1f} uT"
        )

    print("\n=== magnetometer mode comparison ===")
    print("Tilt error is the angle between the filter's attitude and measured")
    print("gravity, over the samples where the head is not accelerating.")
    print("Lower is better; it scores roll and pitch, not yaw.\n")
    print(f"  {'mode':<20} {'mean':>8} {'median':>8} {'p95':>8}   (degrees)")

    scores: list[tuple[float, str]] = []
    for name, mag_input in candidates:
        quaternions = run_madgwick(gyro_remapped, acc_remapped, mag_input, rate_hz)
        stats = tilt_error_vs_gravity(quaternions, acc_remapped)
        if not stats:
            print(f"  {name:<20} too few low-acceleration samples to judge")
            continue
        print(
            f"  {name:<20} {stats['mean']:8.2f} {stats['median']:8.2f} {stats['p95']:8.2f}"
        )
        scores.append((stats["mean"], name))

    if scores:
        scores.sort()
        best_score, best_name = scores[0]
        print(f"\n  best on this recording: {best_name} ({best_score:.2f} deg mean)")
        if best_name == "--no-mag":
            print(
                "  The magnetometer is making the attitude worse, not better —\n"
                "  expected indoors, where steel and motors distort the local field.\n"
                "  Roll and pitch stay absolute without it; only yaw becomes\n"
                "  relative to the recording start, and drifts with gyro bias."
            )


# Decimal places for JSON values. Six is a micro-degree, which is orders of
# magnitude finer than the filter's own accuracy (a few degrees), so nothing
# real is lost — but writing full float repr instead doubles the file size.
JSON_DECIMALS = 6


def write_json_stream(prefix: pathlib.Path, result: dict) -> pathlib.Path:
    """
    Write newline-delimited JSON: one flat object per IMU sample.

    Tobii's cloud streams nest the values under a "payload" key and split
    orientation and angular velocity into separate streams. Neither is done
    here — every value sits at the top level of one object, so a reader needs no
    unwrapping step:

        {"stream_time_s": 0.005992, "roll_deg": 1.495183, ...,
         "roll_deg_s": 2.314005, ...}
    """
    path = prefix.with_suffix(".json")
    keys = (
        "roll_deg",
        "pitch_deg",
        "yaw_deg",
        "roll_deg_s",
        "pitch_deg_s",
        "yaw_deg_s",
    )
    with open(path, "w") as handle:
        for time_s, euler, velocity in zip(
            result["times"], result["euler"], result["angular_velocity"]
        ):
            record = {"stream_time_s": round(float(time_s), JSON_DECIMALS)}
            for key, value in zip(keys, (*euler, *velocity)):
                record[key] = round(float(value), JSON_DECIMALS)
            handle.write(json.dumps(record) + "\n")
    return path


def summarise(result: dict) -> None:
    euler = result["euler"]
    velocity = result["angular_velocity"]
    print("\n=== orientation ===")
    for index, (name, unit) in enumerate(
        [("roll", "deg"), ("pitch", "deg"), ("yaw", "deg")]
    ):
        column = euler[:, index]
        print(
            f"  {name:<5} {unit}: "
            f"min {column.min():9.2f}  max {column.max():9.2f}  "
            f"mean {column.mean():9.2f}"
        )
    speed = np.linalg.norm(velocity, axis=1)
    print(
        f"  angular speed deg/s: median {np.median(speed):.2f}  "
        f"p95 {np.percentile(speed, 95):.2f}  max {speed.max():.2f}"
    )


# ============================ CLI ============================


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Compute head orientation (roll/pitch/yaw) from a raw Tobii Pro "
            "Glasses 3 recording."
        ),
        epilog=(
            "The magnetometer sets absolute heading. If the mean field strength "
            "is far from Earth's 25-65 uT the sensor is uncalibrated: use "
            "--hard-iron auto to estimate and remove the offset, or --no-mag "
            "for relative yaw that drifts but is not distorted."
        ),
    )
    parser.add_argument(
        "recording",
        type=pathlib.Path,
        help="G3 recording folder, or a path to imudata.gz directly",
    )
    parser.add_argument(
        "--out",
        type=pathlib.Path,
        help="output path prefix (default: <recording>/head_orientation)",
    )
    parser.add_argument(
        "--no-mag",
        action="store_true",
        help="ignore the magnetometer: roll/pitch stay absolute, yaw becomes "
        "relative to the recording start and drifts with gyro bias",
    )
    parser.add_argument(
        "--hard-iron",
        choices=["none", "auto"],
        default="none",
        help="magnetometer offset correction. 'none' (default) matches Tobii's "
        "server-side pipeline; 'auto' fits a sphere to estimate and remove a "
        "constant offset, which is needed when the sensor is uncalibrated",
    )
    parser.add_argument(
        "--smooth-ms",
        type=float,
        default=SMOOTH_MS,
        help=f"angular-velocity smoothing window in ms (default {SMOOTH_MS:.0f})",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="score every magnetometer mode against measured gravity and exit "
        "without writing output; run this first to see which mode suits the "
        "recording environment",
    )
    args = parser.parse_args(argv)

    imu_path = resolve_imu_path(args.recording)
    folder = imu_path.parent

    metadata = read_recording_metadata(folder)
    if metadata:
        print(
            f"recording: {metadata.get('name', '?')} "
            f"({metadata.get('duration', 0):.1f} s, "
            f"created {metadata.get('created', '?')})"
        )
    print(f"reading {imu_path}")

    streams = load_g3_imu(imu_path)

    if args.check:
        compare_magnetometer_modes(streams)
        return 0

    result = compute_orientation(
        streams,
        use_magnetometer=not args.no_mag,
        hard_iron=args.hard_iron,
        smooth_ms=args.smooth_ms,
    )

    prefix = args.out or (folder / "head_orientation")
    prefix.parent.mkdir(parents=True, exist_ok=True)
    output_path = write_json_stream(prefix, result)

    summarise(result)
    print(f"\nwrote: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
