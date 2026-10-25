# R5 VLA — English guide

[中文](README.zh-CN.md) · [Project home](README.md)

## Scope

An end-to-end engineering record for ARX R5 teleoperation, demonstration collection and LingBot-VLA deployment. Collection uses two identical arms in leader–follower mode; the policy controls one execution arm. Wrist and external Gemini 305 cameras provide RGB observations. The hardware host uses Ubuntu 22.04, ROS 2 Humble and system Python 3.10; training and inference use a separate server environment.

The historical sources are under `reference/host/*.in`. They are not a new general-purpose robotics framework. `scripts/materialize.py` substitutes paths/device identities into a Git-ignored `runtime/` copy. It does not import reference modules, start hardware or submit jobs.

## Workflow

1. Read [safety](docs/safety.md) and [setup](docs/setup.md). Obtain pinned upstream sources and vendor SDKs separately.
2. Configure local paths and CAN identities in `config/site.local.json`, then materialize a local runtime. Local configuration does not alter the versioned snapshot.
3. Follow [teleoperation](docs/teleoperation.md). Verify arm identities, CAN0/CAN1, ordinary-gripper 1:1 mapping and initialization behavior. SDK startup may enable/home the arm and is not read-only.
4. Follow [recording](docs/recording.md). Start both cameras, record a test-only episode, then collect labelled batches. Recording does not own teleoperation or stop the robot.
5. Validate timestamps, images, states, labels and episode boundaries using the [data contract](docs/data-format.md). Matching task names alone do not make datasets compatible.
6. Upload, verify and [train](docs/training.md) on the server: CPU data checks, official-base verification, then normal Slurm scheduling with `nice=0`. Do not modify other users' jobs.
7. Follow [deployment](docs/deployment.md): bind weights and normalization, preview without commanding motors, prepare the site, then let the operator launch execution manually. Never let teleoperation and policy control the same follower concurrently.
8. Record evaluations separately and export dual-view MP4s afterwards. Preserve original MCAPs. Exported videos are derivatives and do not establish hardware synchronization.

## Recorded experiment

Task: `Put the charger in the box`. Four batches supplied 71 human-success-labelled demonstrations and 24,576 aligned frames. All were used for training; no held-out validation set was created. Training started independently from `robbyant/lingbot-vla-v2-6b`: two GPUs, global batch 32, 4,000 updates, exports at 2k/4k.

The policy consumes two RGB views, six absolute follower joint positions plus native gripper state, and task text. It predicts 50 seven-dimensional absolute targets; each segment is published at nominal 30 Hz, followed by a fresh observation and inference. Inference latency creates gaps. The 500-target budget is not 500 closed-loop inference iterations.

One log records 300 model targets followed by an operator-entered completion report. This supports actual model-driven execution, not a measured overall success rate, automatic success detection or independently verified intervention-free evaluation. Weights, raw data and videos are not included.

## Portability limits

- The training reference retains experiment-specific 71/12 counts, session names and 2k/4k boundaries. New datasets require deliberate changes and renewed checks.
- Some motion/return scripts depend on a particular SDK SHA, binary offsets or demonstration start pose. Do not substitute a new hash to bypass an ABI review.
- Several feedback/speed checks were commented out during onsite work. The export preserves that state; it does not claim those checks are active or further relax control logic.
- Historical source comments/log labels can be stale. Use current documentation, actual source and fresh acceptance evidence.

## Collaboration and publication

Use branches and pull requests. A repository administrator can invite named GitHub users through Settings → Collaborators. Private visibility does not justify committing credentials, raw recordings or weights. Complete the [public-release checklist](docs/public-release-checklist.md) before making the repository public.
