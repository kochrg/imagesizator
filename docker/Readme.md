**Running server:**
- Go to *production-server* folder
- Execute ``docker-compose up``
  *NOTE: If you want to run the container in background run ``docker-compose up -d``.*
- If you make changes in code or in config files of the docker container, a rebuild is needed:
  1. Stop the running containers: ``docker-compose down``.
  2. Run ``docker-compose build`` to rebuild the image.
  3. ``docker-compose up -d`` to start the server again.
