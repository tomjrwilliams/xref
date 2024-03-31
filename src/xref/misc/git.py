import binascii
import pygit2


# ---------------------------------------------------------------


def get_repo(dp="."):
    return pygit2.Repository(dp)


# ---------------------------------------------------------------


def get_branches(dp=".", local=True, remote=True):
    """
    >>> branches = get_branches()
    """
    repo = get_repo(dp=dp)
    if local and remote:
        return list(repo.branches)
    elif local:
        return list(repo.branches.local)
    elif remote:
        return list(repo.branches.remote)
    else:
        raise NotImplementedError()


def get_branch(branch_name, dp="."):
    repo = get_repo(dp=dp)
    branch = repo.branches.get(branch_name)
    return branch


def get_head(dp="."):
    return get_repo(dp=dp).head


# ---------------------------------------------------------------


def get_branch_name(branch=None, dp="."):
    """
    >>> get_branch_name()
    'refs/heads/main'
    """
    if branch is None:
        branch = get_head(dp=dp).resolve()
    else:
        branch = get_branch(branch, dp=dp)
    return branch.name


def get_branch_shorthand(branch=None, dp="."):
    """
    >>> get_branch_shorthand()
    'main'
    """
    if branch is None:
        branch = get_head(dp=dp).resolve()
    else:
        branch = get_branch(branch, dp=dp)
    return branch.shorthand


def get_branch_hash(branch=None, dp="."):
    """
    >>> hsh = get_branch_hash()
    """
    # >>> hsh = get_branch_hash(branch="another_branch")
    if branch is None:
        branch = get_head(dp=dp).resolve()
    else:
        branch = get_branch(branch, dp=dp)
    return str(branch.target)


# ---------------------------------------------------------------
