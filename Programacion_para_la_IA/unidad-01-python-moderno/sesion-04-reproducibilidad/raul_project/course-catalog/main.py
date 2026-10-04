from catalog.__init__ import search_courses
import logging

def main() -> None:
    for course in search_courses("python"):
        print(course.model_dump_json())


if __name__ == "__main__":
    logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s | %(message)s",
)
    main()
