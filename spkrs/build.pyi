from typing import Union, List, Dict

from . import api, solve, storage

class BuildError(RuntimeError): ...
class CollectionError(BuildError): ...

class BinaryPackageBuilder:
    @staticmethod
    def from_spec(spec: api.Spec) -> BinaryPackageBuilder: ...
    def get_solve_graph(self) -> solve.Graph: ...
    def with_source(self, source: Union[str, api.Ident]) -> BinaryPackageBuilder: ...
    def with_option(self, name: str, value: str) -> BinaryPackageBuilder: ...
    def with_options(self, options: api.OptionMap) -> BinaryPackageBuilder: ...
    def with_repository(self, options: storage.Repository) -> BinaryPackageBuilder: ...
    def with_repositories(
        self, repos: List[storage.Repository]
    ) -> BinaryPackageBuilder: ...
    def set_interactive(self, interactive: bool) -> BinaryPackageBuilder: ...
    def get_build_requirements(self) -> List[api.Request]: ...
    def build(self) -> api.Spec: ...

class SourcePackageBuilder:
    @staticmethod
    def from_spec(spec: api.Spec) -> SourcePackageBuilder: ...
    def with_target_repository(
        self, repo: storage.Repository
    ) -> SourcePackageBuilder: ...
    def build(self) -> api.Ident: ...

def validate_build_changeset() -> None: ...
def validate_source_changeset() -> None: ...
def build_options_path(pkg: api.Ident, prefix: str = None) -> str: ...
def build_script_path(pkg: api.Ident, prefix: str = None) -> str: ...
def build_spec_path(pkg: api.Ident, prefix: str = None) -> str: ...
def source_package_path(pkg: api.Ident, prefix: str = None) -> str: ...
def get_package_build_env(spec: api.Spec) -> Dict[str, str]: ...
def data_path(pkg: api.Ident, prefix: str) -> str: ...
def collect_sources(spec: api.Spec, source_dir: str) -> None: ...
