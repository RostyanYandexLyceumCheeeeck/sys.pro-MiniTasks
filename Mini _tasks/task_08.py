from task_05 import specialize


def deprecated(func=None, *, since: str | None = None, will_be_removed: str | None = None):
    if func is None:
        return specialize(deprecated, since=since, will_be_removed=will_be_removed)

    if since and will_be_removed:
        print(f"Warning: function {func.__name__} is deprecated since version {since}. "
              f"It will be removed in version {will_be_removed}.")
    elif since:
        print(f"Warning: function {func.__name__} is deprecated since version {since}. "
              f"It will be removed in future versions.")
    elif will_be_removed:
        print(f"Warning: function {func.__name__} is deprecated. "
              f"It will be removed in version {will_be_removed}.")
    else:
        print(f"Warning: function {func.__name__} is deprecated. It will be removed in future versions.")

    def posrednik(*first_args, **first_kwargs):
        return func(*first_args, **first_kwargs)
    return posrednik


@deprecated(since='123', will_be_removed='qwe')
def foo():
    print('hello, World!')


if __name__ == "__main__":
    foo()
