// Copyright (c) 2021 Sony Pictures Imageworks, et al.
// SPDX-License-Identifier: Apache-2.0
// https://github.com/imageworks/spk

use clap::Parser;
use spfs::Result;
use std::ffi::OsString;

#[macro_use]
mod args;

main!(CmdInit);

#[derive(Parser, Debug)]
pub struct CmdInit {
    #[clap(short, long, parse(from_occurrences))]
    pub verbose: usize,

    /// The root directory of the runtime being initialized
    #[clap(long = "runtime-dir")]
    runtime_root_dir: std::path::PathBuf,

    /// The command to run after initialization
    #[clap(required = true)]
    cmd: Vec<OsString>,
}

impl CmdInit {
    pub async fn run(&mut self, _config: &spfs::Config) -> spfs::Result<i32> {
        tracing::debug!("initializing runtime environment");
        let runtime = spfs::runtime::Runtime::new(&self.runtime_root_dir)?;
        std::env::set_var("SPFS_RUNTIME", runtime.name());
        let owned = spfs::runtime::OwnedRuntime::upgrade(runtime)?;
        let res = self.exec_runtime_command(&owned);
        drop(owned);
        res
    }

    fn exec_runtime_command(&mut self, rt: &spfs::runtime::OwnedRuntime) -> Result<i32> {
        let mut cmd: Vec<_> = self.cmd.drain(..).collect();
        if cmd.is_empty() || cmd[0] == *"" {
            cmd = spfs::build_interactive_shell_cmd(rt)?;
            tracing::debug!("starting interactive shell environment");
        } else {
            cmd =
                spfs::build_shell_initialized_command(rt, cmd[0].clone(), &mut cmd[1..].to_vec())?;
            tracing::debug!("executing runtime command");
        }
        tracing::debug!(?cmd);
        let mut proc = std::process::Command::new(cmd[0].clone());
        proc.args(&cmd[1..]);
        tracing::debug!("{:?}", proc);
        Ok(proc.status()?.code().unwrap_or(1))
    }
}
