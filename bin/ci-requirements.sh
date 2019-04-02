#!/bin/sh

set -e

case "${CIRCLE_BRANCH}" in
	renovate/*)
		echo "Updating requirements." >&2
	;;
	*)
		exit 0
	;;
esac

git config --global user.email "circleci@westnetz.org"
git config --global user.name "Westnetz CircleCI"
make update-requirements
if [ -z "$(git status --porcelain)" ]; then
	exit 0
fi

git commit --all --message "Update requirements"
git push
echo "Failing this build. The branch will be rebuilt because of the update which we just pushed." >&2
exit 1
