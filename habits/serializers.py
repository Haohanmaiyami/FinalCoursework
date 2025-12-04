from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = (
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "linked",
            "period",
            "reward",
            "length",
            "is_public",
            "created",
        )

    def validate(self, attrs):
        linked = attrs.get("linked")
        reward = attrs.get("reward")
        is_pleasant = attrs.get("is_pleasant", False)
        period = attrs.get("period")
        length = attrs.get("length")

        if linked and reward:
            raise serializers.ValidationError(
                "Нельзя одновременно указывать 'linked' и 'reward'. Заполните только одно."
            )
        if length is not None and length > 120:
            raise serializers.ValidationError(
                "Длительность 'length' не может быть больше 120 секунд."
            )
        if linked and not linked.is_pleasant:
            raise serializers.ValidationError(
                "В поле 'linked' можно указать только ПРИЯТНУЮ привычку."
            )
        if is_pleasant and (reward or linked):
            raise serializers.ValidationError(
                "У приятной привычки нельзя указывать 'reward' или 'linked'."
            )
        if period is not None and period > 7:
            raise serializers.ValidationError(
                "Периодичность 'period' должна быть от 1 до 7 дней."
            )
        return attrs
