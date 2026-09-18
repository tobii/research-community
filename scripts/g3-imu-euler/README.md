# Head orientation from a raw Glasses 3 recording

Turns the IMU data in a Tobii Pro Glasses 3 recording folder into head
orientation — roll, pitch, yaw, and angular velocity — using the same Madgwick
AHRS pipeline Tobii runs server-side. It reads the on-glasses files directly, so
no upload or normalization step is involved.

## Install and run

```bash
pip install numpy scipy ahrs

# see which magnetometer mode suits the recording (start here)
python g3_imu_euler.py /path/to/recording --check

# then compute
python g3_imu_euler.py /path/to/recording --no-mag
```

The input is a recording folder (the one holding `recording.g3`), or a path to
`imudata.gz` directly. Output goes beside the recording as
`head_orientation.json`, or wherever `--out` points.

| Option | Effect |
| :-- | :-- |
| `--check` | Score every magnetometer mode against gravity, write nothing |
| `--no-mag` | Ignore the magnetometer — see [Magnetometer](#the-magnetometer-read-this) |
| `--hard-iron auto` | Estimate and remove a constant magnetometer offset |
| `--out PREFIX` | Output path prefix |
| `--smooth-ms MS` | Angular-velocity smoothing window, default 250 ms |

## Input format

A G3 recording folder looks like this. Only the first two files are needed here:

| File | Contents |
| :-- | :-- |
| `imudata.gz` | IMU samples — **the input to this script** |
| `recording.g3` | Manifest: duration, camera calibration, timestamps (optional) |
| `gazedata.gz` | Gaze samples |
| `scenevideo.mp4` | Scene camera video |
| `meta/` | Serial numbers, participant, user events |

`imudata.gz` is gzipped newline-delimited JSON. Each line is **one sample of one
sensor**, and the sensors are interleaved rather than aligned:

```json
{"type":"imu","timestamp":0.005992,"data":{"accelerometer":[-0.250,9.689,-1.427],"gyroscope":[-1.294,-0.345,1.037]}}
{"type":"imu","timestamp":0.067795,"data":{"magnetometer":[300.199,-339.889,167.661]}}
```

So a line carries accelerometer **and** gyroscope, or magnetometer alone. A
reader must not assume every line has every field — that is the single most
common mistake when parsing these files.

| Sensor | Rate | Units as written | Notes |
| :-- | :-- | :-- | :-- |
| `accelerometer` | ~118 Hz | m/s² | Co-timestamped with the gyroscope |
| `gyroscope` | ~118 Hz | **degrees/s** | Converted to rad/s by this script |
| `magnetometer` | ~10 Hz | µT | ~12× slower, interpolated onto the gyro timeline |

`timestamp` is seconds from the start of the recording.

Rates above are measured from the sample recording; treat them as typical, not
guaranteed. The script derives the true rate from the timestamps.

## Output format

Newline-delimited JSON: one flat object per IMU sample, every value at the top
level.

```json
{"stream_time_s": 0.005992, "roll_deg": 1.495183, "pitch_deg": 8.374632, "yaw_deg": 0.217814, "roll_deg_s": 2.314005, "pitch_deg_s": -1.215876, "yaw_deg_s": 0.264203}
```

| Field | Meaning |
| :-- | :-- |
| `stream_time_s` | Seconds from the start of the recording |
| `roll_deg`, `pitch_deg`, `yaw_deg` | Orientation, degrees |
| `roll_deg_s`, `pitch_deg_s`, `yaw_deg_s` | Rate of change, degrees/second |

Newline-delimited rather than one big array, so a long recording streams line by
line instead of being held in memory whole. Values are rounded to six decimals —
a micro-degree, far below the filter's own accuracy of a few degrees.

```python
import pandas as pd
df = pd.read_json("head_orientation.json", lines=True)   # ready to use, no unwrapping
```

Note this is *flatter* than Tobii's cloud data streams, which nest the values
under a `payload` key and split orientation and angular velocity into two
separate streams. If you need to match those exactly, nest each record's values
under `payload` and split on the `_deg` / `_deg_s` suffix.

## Conventions

**Coordinate system.** G3 reports IMU data in the head unit coordinate system
(HUCS), right-handed, `X = Left, Y = Up, Z = Forward`. Confirmed on the sample
recording: the mean accelerometer reading is `[0.1, 9.1, -1.8] m/s²`, i.e.
gravity on +Y.

**Euler angles**, after the sign convention Tobii applies:

| Angle | Positive means | Range |
| :-- | :-- | :-- |
| `roll` | Right ear down | ±180° |
| `pitch` | Looking **down** | ±90° |
| `yaw` | Turning **left** | unwrapped, accumulates past ±180° |

Yaw is unwrapped rather than wrapped, so a full turn reads 360° instead of
jumping back to 0. Subtract multiples of 360° if you want a compass-style
heading.

**Angular velocity** is the frame-to-frame Euler difference, moving-average
smoothed and scaled to degrees/second. The window is 250 ms by default,
expressed in time rather than samples so it means the same thing on G3 (~118 Hz)
and Glasses X (~400 Hz).

## The magnetometer — read this

An AHRS filter fuses three sensors. The gyroscope integrates rotation, the
accelerometer corrects tilt against gravity, and the magnetometer corrects
heading against magnetic north. Drop the magnetometer and **roll and pitch stay
absolute**, because gravity still observes them; only yaw becomes relative to
the recording start, and drifts slowly with gyro bias.

That trade is often worth making, because the magnetometer assumes the only
magnetic field present is Earth's. Indoors that assumption fails — steel
shelving, refrigeration units and motors all distort the local field, and the
distortion varies from place to place, so it cannot be calibrated away with a
fixed offset.

On the sample recording (a convenience store) the magnetometer reads a mean
field strength of **472 µT** against Earth's 25–65 µT. Scored against gravity,
the three modes come out:

| Mode | Tilt error vs gravity (mean) |
| :-- | :-- |
| `--no-mag` | **6.3°** |
| `--hard-iron auto` | 12.9° |
| default, raw magnetometer | 16.9° |

The magnetometer makes the attitude two to three times worse. `--hard-iron auto`
recovers a plausible field strength (25.7 µT) and helps, but cannot fix a
disturbance that varies with position.

This is why `--check` exists and why it is worth running first: which mode wins
is a property of the recording environment, not of the glasses. Outdoors or in a
building without much steel, the magnetometer should win and give you
non-drifting absolute heading.

**How `--check` decides.** While the head is not accelerating, the accelerometer
direction *is* the up-vector — so it can referee the filter. The script rotates
the filter's own idea of world-up into the body frame and measures the angle to
the measured up-vector, over samples within 0.3 m/s² of 1 g. That is
independent of every Euler sign convention, and it scores roll and pitch. It
cannot score yaw, because nothing in the recording observes absolute heading
except the magnetometer being tested.

## Differences from Tobii's server-side pipeline

The filter, gain (`beta = 0.04`), axis remapping, sign conventions and yaw
unwrapping all match. Three things differ, all consequences of reading raw files
rather than normalized ones:

1. **Gyroscope units.** G3 writes degrees/s; the cloud format stores radians/s.
   This script converts, as the server-side normalizer does.
2. **Smoothing window.** The server-side pipeline hard-codes 100 samples, which
   is ~250 ms at the Glasses X rate of ~400 Hz but ~850 ms at G3's ~118 Hz. This
   script expresses the window in milliseconds and derives the sample count from
   the measured rate, so smoothing is equivalent on both devices.
3. **Magnetometer modes.** `--no-mag` and `--hard-iron auto` have no
   server-side equivalent; the default matches it.

The output shape also differs — see the note under
[Output format](#output-format).
