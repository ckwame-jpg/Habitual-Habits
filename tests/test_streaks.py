from datetime import date, timedelta


def _create_habit(client, auth_header):
    resp = client.post("/habits/", json={"title": "Exercise", "frequency": "daily"}, headers=auth_header)
    return resp.json()["id"]


def _complete_on(client, auth_header, habit_id, d):
    client.post(f"/habits/{habit_id}/complete", json={"date_completed": d.isoformat()}, headers=auth_header)


def test_streak_no_completions(client, auth_header):
    habit_id = _create_habit(client, auth_header)
    resp = client.get(f"/habits/{habit_id}/streak", headers=auth_header)
    assert resp.json()["streak"] == 0


def test_streak_one_day(client, auth_header):
    habit_id = _create_habit(client, auth_header)
    _complete_on(client, auth_header, habit_id, date.today())
    resp = client.get(f"/habits/{habit_id}/streak", headers=auth_header)
    assert resp.json()["streak"] == 1


def test_streak_consecutive_days(client, auth_header):
    habit_id = _create_habit(client, auth_header)
    today = date.today()
    _complete_on(client, auth_header, habit_id, today)
    _complete_on(client, auth_header, habit_id, today - timedelta(days=1))
    _complete_on(client, auth_header, habit_id, today - timedelta(days=2))
    resp = client.get(f"/habits/{habit_id}/streak", headers=auth_header)
    assert resp.json()["streak"] == 3


def test_streak_with_gap(client, auth_header):
    habit_id = _create_habit(client, auth_header)
    today = date.today()
    _complete_on(client, auth_header, habit_id, today)
    # Skip yesterday, complete 2 days ago
    _complete_on(client, auth_header, habit_id, today - timedelta(days=2))
    resp = client.get(f"/habits/{habit_id}/streak", headers=auth_header)
    assert resp.json()["streak"] == 1
