from main import app


def test_my_ratings_route_is_registered_once():
    registrations = [
        route
        for route in app.routes
        if getattr(route, "path", None) == "/ratings/me"
        and "GET" in getattr(route, "methods", set())
    ]

    assert len(registrations) == 1
