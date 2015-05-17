if [ -n "${TRAVIS_BRANCH+1}" ]; then
  continue
else
  redis-server &
fi

py.test --cov-report term-missing --cov-config .coveragerc --cov . --boxed -n14 -k 'not functional' tests/

if [ -n "${TRAVIS_BRANCH+1}" ]; then
  continue
else
  redis-cli shutdown
fi
