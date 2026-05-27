#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "classq.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django를 불러올 수 없습니다. 가상환경을 활성화했는지 확인해주세요."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
