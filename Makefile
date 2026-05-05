migrate:
	docker compose -f compose.dev.yaml exec wagtail python manage.py migrate
makemigrations:
	docker compose -f compose.dev.yaml exec wagtail python manage.py makemigrations
up:
	docker compose -f compose.dev.yaml up --build
down:
	docker compose -f compose.dev.yaml down
css:
	npx @tailwindcss/cli -i ./jano/static/css/input.css -o ./jano/static/css/output.css --watch
