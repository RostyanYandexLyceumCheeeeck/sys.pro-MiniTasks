from setuptools import Extension, setup

setup(
    name="foreign",
    version="1.0.0",
    description="Python interface for Matrix exponentiation from C",
    author="dbg",
    author_email="r.zagitov@g.nsu.ru",
    ext_modules=[
        Extension(
            name="foreign",
            sources=["foreignmodule.c"],
        ),
    ]
)
