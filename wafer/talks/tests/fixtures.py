from wafer.talks.models import Talk, TalkType
from wafer.tests.utils import create_user


def create_talk_type(name, **kwargs):
    """Create a talk type"""
    return TalkType.objects.create(name=name, **kwargs)


def create_talk(title, status, username=None, user=None, talk_type=None,
                talk_track=None, language=None):
    if sum((user is None, username is None)) != 1:
        raise ValueError('One of user OR username must be specified')
    if username:
        user = create_user(username)
    talk = Talk.objects.create(
        title=title, status=status, corresponding_author_id=user.id)
    talk.authors.add(user)
    talk.notes = "Some notes for talk %s" % title
    talk.private_notes = "Some private notes for talk %s" % title
    talk.save()
    if talk_type:
        talk.talk_type = talk_type
        talk.save()
    if talk_track:
        talk.track = talk_track
        talk.save()
    if language:
        talk.language = language
        talk.save()
    return talk
