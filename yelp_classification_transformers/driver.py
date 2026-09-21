"""
Single entry point for the Yelp classification project.

This driver uses the existing project files rather than duplicating their code.
"""
from helper import execute, terminate_signal
terminate_signal()
import yelp
import model_build
import report


def main():
    yelp.main()

    report.main()

    model_build.main()


if __name__ == "__main__":
    execute(main)
