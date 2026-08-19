# Profiles and resolution

A profile selects which owned capabilities are available in one operating context. A resolution is the derived view used for routing or runtime checks.

## Reference flow

1. Start from a validated registry.
2. Select one profile.
3. Include skills whose ownership is allowed and whose identifiers are explicitly enabled.
4. Preserve global router discoverability where the host architecture requires it.
5. Record unavailable targets with a reason.
6. Compare the stored resolution with a fresh compile before treating it as current.

The committed [profile-resolution.json](../../architecture/examples/profile-resolution.json) is fictional. It exists to show the shape of a safe public example.

## Static versus runtime truth

A registry compiler can prove that inputs are structurally coherent. It cannot prove that a live host loaded the expected files, that plugin state matches the registry, or that activation occurred. Runtime claims need current host evidence.

For that reason, this repository does not publish a live profile snapshot or claim parity with any private resolver. A future public compiler should remain blocked until it can operate entirely on synthetic/public fixtures and has independent compatibility evidence.
