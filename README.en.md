# R5 VLA — English guide

[中文](README.zh-CN.md) · [Project home](README.md)

## Scope

An end-to-end engineering record for ARX R5 teleoperation, demonstration collection and LingBot-VLA deployment. Collection uses two identical arms in leader–follower mode; the policy controls one execution arm. Wrist and external Gemini 305 cameras provide RGB observations. The hardware host uses Ubuntu 22.04, ROS 2 Humble and system Python 3.10; training and inference use a separate server environment.

Source templates live in `reference/host/*.in`. `scripts/materialize.py` substitutes local paths and device identities to generate `runtime/`. Local configuration and runtime artifacts are Git-ignored.

## Workflow

1. [Install dependencies](docs/setup.md): ROS 2, vendor SDKs, camera drivers and the training environment.
2. Configure `config/site.local.json` and generate the runtime directory.
3. [Start teleoperation](docs/teleoperation.md): leader on `can0`, follower on `can1`, ordinary-gripper mapping at 1:1.
4. [Record demonstrations](docs/recording.md): start both cameras, run a test-only recording, then collect and label batches.
5. [Process data](docs/data-format.md): validate messages, timestamps and labels, then align RGB views and follower state.
6. [Train](docs/training.md): prepare data, verify the base model and run two-GPU training on the server.
7. [Deploy](docs/deployment.md): start inference, establish the SSH tunnel, preview predictions and execute the policy.
8. Record evaluations separately and export dual-view MP4s.

See [safety](docs/safety.md) for hardware startup and control-mode switching.

## Recorded experiment

Task: `Put the charger in the box`. Four batches supplied 71 human-success-labelled demonstrations and 24,576 aligned frames. All were used for training; no held-out validation set was created. Training started independently from `robbyant/lingbot-vla-v2-6b`: two GPUs, global batch 32, 4,000 updates, exports at 2k/4k.

The policy consumes two RGB views, six absolute follower joint positions plus native gripper state, and task text. It predicts 50 seven-dimensional absolute targets; each segment is published at nominal 30 Hz, followed by a fresh observation and inference. Inference latency creates gaps. The 500-target budget is not 500 closed-loop inference iterations.

One test records 300 model targets before the operator ended the run and marked completion. Automatic success detection and an aggregate success-rate evaluation are not implemented; see the [experiment record](docs/provenance.md).

## Adapting to a new environment

- Update session lists, the experiment-specific 71/12 episode counts and 2k/4k settings when changing datasets.
- Some motion/return tools depend on a particular SDK SHA, binary layout and demonstration start pose.
- Current feedback-check behavior is documented in [safety](docs/safety.md).
