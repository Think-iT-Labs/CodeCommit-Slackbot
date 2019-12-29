from events import ReferenceCreated, ReferenceUpdated, ReferenceDeleted, \
    PullRequestCreatedEvent, PullRequestStatusChangedEvent, \
    PullRequestMergeStatusUpdatedEvent, CommentOnCommitCreatedEvent, \
    CommentOnCommitUpdatedEvent, CommentOnPullRequestCreatedEvent, \
    CommentOnPullRequestUpdatedEvent


class EventFactory(object):
    def __init__(self, event):
        self.event = event

    def get_instance(self):
        event_type = self.event['detail']['event']

        if event_type == 'referenceCreated':
            return ReferenceCreated(self.event)
        elif event_type == 'referenceUpdated':
            return ReferenceUpdated(self.event)
        elif event_type == 'referenceDeleted':
            return ReferenceDeleted(self.event)
        elif event_type == 'pullRequestCreated':
            return PullRequestCreatedEvent(self.event)
        elif event_type == 'pullRequestStatusChanged':
            return PullRequestStatusChangedEvent(self.event)
        elif event_type == 'pullRequestMergeStatusUpdated':
            return PullRequestMergeStatusUpdatedEvent(self.event)
        elif event_type == 'commentOnCommitCreated':
            return CommentOnCommitCreatedEvent(self.event)
        elif event_type == 'commentOnCommitUpdated':
            return CommentOnCommitUpdatedEvent(self.event)
        elif event_type == 'commentOnPullRequestCreated':
            return CommentOnPullRequestCreatedEvent(self.event)
        elif event_type == 'commentOnPullRequestUpdated':
            return CommentOnPullRequestUpdatedEvent(self.event)
