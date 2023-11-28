from task_05 import specialize


def deprecated(func=None, *, since: str | None = None, will_be_removed: str | None = None):
    if func is None:
        return specialize(deprecated, since=since, will_be_removed=will_be_removed)

    st_since = f" since version {since}" if since else ""
    st_will = f"version {will_be_removed}." if will_be_removed else "future versions."

    print(f"Warning: function {func.__name__} is deprecated{st_since}. " 
          f"It will be removed in {st_will}")

    def posrednik(*first_args, **first_kwargs):
        return func(*first_args, **first_kwargs)
    return posrednik


@deprecated(since='123', will_be_removed=None)
def foo():
    print('hello, World!')


if __name__ == "__main__":
    foo()
