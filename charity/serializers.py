from django.forms import ValidationError
from rest_framework import serializers
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Charity,Donations,CharityPhases
from django.db import models

class CharityPhase_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CharityPhases
        fields = ["description","amount"]

class Charity_Serializer(serializers.ModelSerializer):
    charity_phases = CharityPhase_Serializer(many=True,read_only=True)
    remaining_amount = serializers.SerializerMethodField()
    
    class Meta:
        model = Charity
        fields = "__all__"
        read_only_fields = ('user',)

    def get_remaining_amount(self,obj):
        total_donated = obj.donations.aggregate(total = models.Sum('amount'))['total'] or 0
        return obj.amount_needed - total_donated

    def validate(self, attrs):
        user = self.context['request'].user
        existing_charity = Charity.objects.filter(
            user = user,
            deadline__gt = timezone.now().date()
        ).exclude(pk = self.instance.pk if self.instance else None)

        if existing_charity:
            raise serializers.ValidationError({"error":"you already have active charity"})
            
        return attrs
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
class BulkPhase_Serializer(serializers.ListSerializer):
    def create(self, validated_data):
        charity_id = validated_data[0]["charity_id"]
        charity = Charity.objects.get(id=charity_id)

        phases = [
            CharityPhases(
                charity=charity,
                description = item["description"],
                amount = item["amount"]
            )for item in validated_data
        ]
        return CharityPhases.objects.bulk_create(phases)
    
class CreateCharityPhase_Serializer(serializers.ModelSerializer):
    charity_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CharityPhases
        fields = ["charity_id","description","amount"]
        list_serializer_class = BulkPhase_Serializer
    
class CharityMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charity
        fields = ["id","name"]

class ViewDonation(serializers.ModelSerializer):
    charity = CharityMinSerializer(read_only=True)

    class Meta:
        model = Donations
        fields = ["amount","phone","vendor","charity"]

class Donate_Serializer(serializers.ModelSerializer):
    charity_id = serializers.IntegerField(write_only=True)
    amount = serializers.DecimalField(max_digits=11, decimal_places=2)
    phone = serializers.CharField(max_length=20)
    vendor = serializers.ChoiceField(choices=Donations.VENDOR_CHOICE)

    class Meta:
        model = Donations
        fields = ["charity_id","amount","phone","vendor"]

    def validate(self, attrs):
        charity_id = attrs.get("charity_id")
        charity = get_object_or_404(Charity, id=charity_id)

        donation = Donations(
            charity = charity,
            amount = attrs["amount"],
            phone = attrs["phone"],
            vendor = attrs["vendor"],
            user = self.context["request"].user
        )
        donation.clean()
        return attrs
    
    def create(self,validated_data):
        user = self.context["request"].user
        charity = get_object_or_404(Charity,id=validated_data.pop("charity_id"))
        
        return Donations.objects.create(
            user = user,
            charity=charity,
            ** validated_data
        )