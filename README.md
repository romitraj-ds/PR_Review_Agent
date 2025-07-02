## Enviroment Setup
Update the env variables with real keys

## Duild a docker image
```bash
docker build -t pr-reviewer:0.0.1 .
```

## Run the docker as service
```bash
docker run --rm -p 8000:8000 pr-reviewer:0.0.1
```

## Ask service to review PR
```bash
curl -X POST http://localhost:8000/review \
  -H "Content-Type: application/json" \
  -d '{"question": "Analyse and comment on PR: https://github.com/<owner>/<repo>/pull/<number>"}'
```

## Response
- The AI will return a review comment in the terminal.
- The same comment will also be posted directly on the GitHub Pull Request as a comment.

![Review Example](assets/review_example.png)
