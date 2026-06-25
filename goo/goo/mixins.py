class ProfileNameMixin:
    @property
    def display_name(self):
        full_name = self.get_full_name()
        return full_name or self.username


class ProfileAdminSummaryMixin:
    @property
    def profile_summary_label(self):
        return 'Profile summary'

    def profile_summary(self, obj):
        parts = [obj.display_name]
        if obj.city:
            parts.append(obj.city)
        if obj.phone_number:
            parts.append(obj.phone_number)
        return ' | '.join(parts)
