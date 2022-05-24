**For dev server:**
- Go to *server-dev* folder
- Execute ``docker-compose up``

**For staging server:**
- Go to *server-staging* folder
- Execute ``docker-compose up``

**NOTE:**
If ERROR ``'can't stat 'some-url/imagesizator/docker/dockerfiles/postgresql/data''`` appears when
execute ``docker-compose up`` then open a terminal and go to *docker* folder.

SOLUTION:

1) Run ``sudo chmod 777 -R ./dockerfiles/postgresql/data``

2) Run ``docker-compose up``

If you want to run the containers in background run ``docker-compose up -d``.
