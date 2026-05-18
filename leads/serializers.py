from rest_framework import serializers

from .models import Lead


class LeadCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lead

        fields = [
            "full_name",
            "email",
            "company_name",
            "website",
            "industry",
            "business_goal",
        ]

    def validate_full_name(self, value):

        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "Full name is too short."
            )

        return value

    def validate_company_name(self, value):

        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "Company name is too short."
            )

        return value

    def validate_website(self, value):

        if not value.startswith(("http://", "https://")):
            raise serializers.ValidationError(
                "Website must start with http:// or https://"
            )

        return value

    def validate_business_goal(self, value):

        if len(value) > 1000:
            raise serializers.ValidationError(
                "Business goal is too long."
            )

        return value