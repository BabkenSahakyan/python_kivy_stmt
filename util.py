import json


def write_json(user, score, t_num):
    with open('scores.json') as f:
        jd = json.load(f)

    lis = list()
    if user in jd:
        lis = jd[user]
    lis += [[score / 10, t_num]]
    jd[user] = lis

    with open('scores.json', 'w') as f:
        json.dump(jd, f)


def get_user_score(user):
    with open('scores.json') as f:
        jd = json.load(f)

    return jd[user]


def get_user_attempts_count(user):
    return len(get_user_score(user))


if __name__ == '__main__':
    print(get_user_attempts_count('admin'))
