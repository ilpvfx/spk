use rstest::rstest;

use super::{Entry, Manifest};
use crate::{
    encoding::{self, Encodable},
    tracking,
};

fixtures!();

#[rstest]
#[tokio::test]
async fn test_entry_blobs_compare_name() {
    let a = Entry {
        name: "a".to_string(),
        kind: tracking::EntryKind::Blob,
        mode: 0,
        object: encoding::EMPTY_DIGEST.into(),
        size: 0,
    };
    let b = Entry {
        name: "b".to_string(),
        kind: tracking::EntryKind::Blob,
        mode: 0,
        object: encoding::EMPTY_DIGEST.into(),
        size: 0,
    };
    assert!(a < b);
    assert!(b > a);
}

#[rstest]
#[tokio::test]
async fn test_entry_trees_compare_name() {
    let a = Entry {
        name: "a".to_string(),
        kind: tracking::EntryKind::Tree,
        mode: 0,
        object: encoding::EMPTY_DIGEST.into(),
        size: 0,
    };
    let b = Entry {
        name: "b".to_string(),
        kind: tracking::EntryKind::Tree,
        mode: 0,
        object: encoding::EMPTY_DIGEST.into(),
        size: 0,
    };
    assert!(a < b);
    assert!(b > a);
}

#[rstest]
#[tokio::test]
async fn test_entry_compare_kind() {
    let blob = Entry {
        name: "a".to_string(),
        kind: tracking::EntryKind::Blob,
        mode: 0,
        object: encoding::EMPTY_DIGEST.into(),
        size: 0,
    };
    let tree = Entry {
        name: "b".to_string(),
        kind: tracking::EntryKind::Tree,
        mode: 0,
        object: encoding::EMPTY_DIGEST.into(),
        size: 0,
    };
    assert!(tree > blob);
    assert!(blob < tree);
}

#[rstest]
#[tokio::test]
async fn test_entry_compare() {
    let root_file = Entry {
        name: "file".to_string(),
        kind: tracking::EntryKind::Blob,
        mode: 0,
        object: encoding::NULL_DIGEST.into(),
        size: 0,
    };
    let root_dir = Entry {
        name: "xdir".to_string(),
        kind: tracking::EntryKind::Tree,
        mode: 0,
        object: encoding::NULL_DIGEST.into(),
        size: 0,
    };
    assert!(root_dir > root_file);
}
