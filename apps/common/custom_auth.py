from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        try:
            user = User.objects.get(**{self.username_field: attrs[self.username_field]})
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "No account found with this email address."
            )

        # If  the user exists, try to authenticate
        self.user = authenticate(**authenticate_kwargs)

        if self.user is None:
            raise serializers.ValidationError("Incorrect password. Please try again.")

        if not self.user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        if not self.user.is_verified:
            raise serializers.ValidationError(
                "User is not verified"
            )

        return super().validate(attrs)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
