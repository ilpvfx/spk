// Copyright (c) 2021 Sony Pictures Imageworks, et al.
// SPDX-License-Identifier: Apache-2.0
// https://github.com/imageworks/spk
//! Remote server implementations of the spfs repository
use std::sync::Arc;

use tokio_stream::StreamExt;
use tonic::{Request, Response, Status};

use proto::repository_server::{Repository, RepositoryServer};
pub mod proto {
    tonic::include_proto!("spfs");
}

use crate::storage;

#[derive(Debug, Clone)]
pub struct Service {
    repo: Arc<storage::RepositoryHandle>,
}

#[tonic::async_trait]
impl Repository for Service {
    async fn ping(
        &self,
        _request: Request<proto::PingRequest>,
    ) -> std::result::Result<Response<proto::PingResponse>, Status> {
        let data = proto::PingResponse::default();
        Ok(Response::new(data))
    }

    async fn ls_tags(
        &self,
        request: Request<proto::LsTagsRequest>,
    ) -> std::result::Result<Response<proto::LsTagsResponse>, Status> {
        let request = request.into_inner();
        let path = relative_path::RelativePathBuf::from(&request.path);
        let entries: crate::Result<Vec<_>> = {
            self.repo.ls_tags(&path).collect().await
        };

        let data = proto::LsTagsResponse {
            entries: entries.unwrap(),
        };
        Ok(Response::new(data))
    }
}

impl Service {
    pub fn new_srv(repo: storage::RepositoryHandle) -> RepositoryServer<Self> {
        RepositoryServer::new(Self {
            repo: Arc::new(repo),
        })
    }
}
