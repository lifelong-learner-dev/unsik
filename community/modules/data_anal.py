from django.conf import settings
import joblib

def female_senior_input_predict(s_r, c_s, t_s, g_l, g_r):
    file_path = settings.BASE_DIR / 'community' / 'modules'
    loaded_model = joblib.load(file_path / 'female_senior_model.pkl')
    pred = loaded_model.predict([[s_r, c_s, t_s, g_l, g_r]])

    if pred[0] == 3:
        result = '✨🎉🎊 오~ 1등급입니다! 대단하시네요! 🏆🥇🏅'
    elif pred[0] == 2:
        result = '🎉🎊 2등급입니다! 축하드립니다! 🥈'
    elif pred[0] == 1:
        result = '🎉🎊 3등급입니다 🥉'
    else:
        result = '좀 더 노력하세요! 참가증만 받으실 수 있어요 😅'

    return result


def female_adult_input_predict(c_s, s_r, s_l_j, s_o, g_l, g_r):
    file_path = settings.BASE_DIR / 'community' / 'modules'
    loaded_model = joblib.load(file_path / 'female_adult_model.pkl')
    pred = loaded_model.predict([[c_s, s_r, s_l_j, s_o, g_l, g_r]])

    if pred[0] == 3:
        result = '✨🎉🎊 오~ 1등급입니다! 대단하시네요! 🏆🥇🏅'
    elif pred[0] == 2:
        result = '🎉🎊 2등급입니다! 축하드립니다! 🥈'
    elif pred[0] == 1:
        result = '🎉🎊 3등급입니다 🥉'
    else:
        result = '좀 더 노력하세요! 참가증만 받으실 수 있어요 😅'

    return result


def female_adolescent_input_predict(s_r, s_rn, r_j, s_l_j, h_t):
    file_path = settings.BASE_DIR / 'community' / 'modules'
    loaded_model = joblib.load(file_path / 'female_adolescent_model.pkl')
    pred = loaded_model.predict([[s_r, s_rn, r_j, s_l_j, h_t]])

    if pred[0] == 3:
        result = '✨🎉🎊 오~ 1등급입니다! 대단하시네요! 🏆🥇🏅'
    elif pred[0] == 2:
        result = '🎉🎊 2등급입니다! 축하드립니다! 🥈'
    elif pred[0] == 1:
        result = '🎉🎊 3등급입니다 🥉'
    else:
        result = '좀 더 노력하세요! 참가증만 받으실 수 있어요 😅'

    return result


def female_child_input_predict(s_r, s_u, s_l_j, s_rn):
    file_path = settings.BASE_DIR / 'community' / 'modules'
    loaded_model = joblib.load(file_path / 'female_child_model.pkl')
    pred = loaded_model.predict([[s_r, s_u, s_l_j, s_rn]])

    if pred[0] == 3:
        result = '✨🎉🎊 오~ 1등급입니다! 대단하시네요! 🏆🥇🏅'
    elif pred[0] == 2:
        result = '🎉🎊 2등급입니다! 축하드립니다! 🥈'
    elif pred[0] == 1:
        result = '🎉🎊 3등급입니다 🥉'
    else:
        result = '좀 더 노력하세요! 참가증만 받으실 수 있어요 😅'

    return result



def male_senior_input_predict(s_r, c_s, t_s, g_l, g_r):
    file_path = settings.BASE_DIR / 'community' / 'modules'
    loaded_model = joblib.load(file_path / 'male_senior_model.pkl')
    pred = loaded_model.predict([[s_r, c_s, t_s, g_l, g_r]])

    if pred[0] == 3:
        result = '✨🎉🎊 오~ 1등급입니다! 대단하시네요! 🏆🥇🏅'
    elif pred[0] == 2:
        result = '🎉🎊 2등급입니다! 축하드립니다! 🥈'
    elif pred[0] == 1:
        result = '🎉🎊 3등급입니다 🥉'
    else:
        result = '좀 더 노력하세요! 참가증만 받으실 수 있어요 😅'

    return result


def male_adult_input_predict(c_s, s_r, s_l_j, s_o, g_l, g_r):
    file_path = settings.BASE_DIR / 'community' / 'modules'
    loaded_model = joblib.load(file_path / 'male_adult_model.pkl')
    pred = loaded_model.predict([[c_s, s_r, s_l_j, s_o, g_l, g_r]])

    if pred[0] == 3:
        result = '✨🎉🎊 오~ 1등급입니다! 대단하시네요! 🏆🥇🏅'
    elif pred[0] == 2:
        result = '🎉🎊 2등급입니다! 축하드립니다! 🥈'
    elif pred[0] == 1:
        result = '🎉🎊 3등급입니다 🥉'
    else:
        result = '좀 더 노력하세요! 참가증만 받으실 수 있어요 😅'

    return result


def male_adolescent_input_predict(s_r, s_rn, r_j, s_l_j, h_t):
    file_path = settings.BASE_DIR / 'community' / 'modules'
    loaded_model = joblib.load(file_path / 'male_adolescent_model.pkl')
    pred = loaded_model.predict([[s_r, s_rn, r_j, s_l_j, h_t]])

    if pred[0] == 3:
        result = '✨🎉🎊 오~ 1등급입니다! 대단하시네요! 🏆🥇🏅'
    elif pred[0] == 2:
        result = '🎉🎊 2등급입니다! 축하드립니다! 🥈'
    elif pred[0] == 1:
        result = '🎉🎊 3등급입니다 🥉'
    else:
        result = '좀 더 노력하세요! 참가증만 받으실 수 있어요 😅'

    return result


def male_child_input_predict(s_r, s_u, s_l_j, s_rn):
    file_path = settings.BASE_DIR / 'community' / 'modules'
    loaded_model = joblib.load(file_path / 'male_child_model.pkl')
    pred = loaded_model.predict([[s_r, s_u, s_l_j, s_rn]])

    if pred[0] == 3:
        result = '✨🎉🎊 오~ 1등급입니다! 대단하시네요! 🏆🥇🏅'
    elif pred[0] == 2:
        result = '🎉🎊 2등급입니다! 축하드립니다! 🥈'
    elif pred[0] == 1:
        result = '🎉🎊 3등급입니다 🥉'
    else:
        result = '좀 더 노력하세요! 참가증만 받으실 수 있어요 😅'

    return result
