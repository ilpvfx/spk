// Copyright (c) Sony Pictures Imageworks, et al.
// SPDX-License-Identifier: Apache-2.0
// https://github.com/spkenv/spk

pub use {
    spk_build as build,
    spk_exec as exec,
    spk_schema as schema,
    spk_solve as solve,
    spk_storage as storage,
};

pub const VERSION: &str = env!("CARGO_PKG_VERSION");
