migrate:
	docker compose -f compose.dev.yaml exec wagtail python manage.py migrate
makemigrations:
	docker compose -f compose.dev.yaml exec wagtail python manage.py makemigrations
up:
	docker image prune -f
	docker compose -f compose.dev.yaml up --build
down:
	docker compose -f compose.dev.yaml down
	docker image prune -f
css:
	npx @tailwindcss/cli -i ./core/static/css/input.css -o ./core/static/css/output.css --watch
