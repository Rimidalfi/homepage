migrate:
	docker compose -f compose.dev.yaml exec wagtail python manage.py migrate
makemigrations:
	docker compose -f compose.dev.yaml exec wagtail python manage.py makemigrations
up:
	docker compose -f compose.dev.yaml up --build
down:
	docker compose -f compose.dev.yaml down
dev:
	docker compose -f compose.dev.yaml up -d
	npx @tailwindcss/cli -i ./home/static/css/input.css -o ./home/static/css/output.css --watch
