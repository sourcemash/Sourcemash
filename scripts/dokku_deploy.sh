if ([ "$TRAVIS_PULL_REQUEST" == "false" ] && [ "$TRAVIS_BRANCH" == "production" ]); then
  echo -e "Host sourcemash.com\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config
  chmod 600 config/deploy_id_rsa
  eval `ssh-agent -s`
  ssh-add config/deploy_id_rsa
  git remote add dokku dokku@sourcemash.com:sourcemash
  git push dokku production:master
  ssh root@sourcemash.com "dokku run sourcemash python manage.py db upgrade; dokku run sourcemash python manage.py assets clean; dokku run sourcemash python manage.py assets build"
fi
