from django.db import models

class FoodItem(models.Model):
    food_id = models.AutoField(primary_key=True)
    food_code = models.IntegerField(null=True, blank=True)
    food_group_id = models.IntegerField(null=True, blank=True)
    food_source_id = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    description_french = models.TextField(null=True, blank=True)
    date_of_entry = models.DateField(null=True, blank=True)
    date_of_publication = models.DateField(null=True, blank=True)
    country_code = models.IntegerField(null=True, blank=True)
    scientific_name = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.description

class Nutrient(models.Model):
    nutrient_id = models.IntegerField(primary_key=True)
    nutrient_code = models.IntegerField(null=True, blank=True)
    symbol = models.CharField(max_length=50, null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=255)
    name_french = models.CharField(max_length=255, null=True, blank=True)
    tag_name = models.CharField(max_length=50, null=True, blank=True)
    decimal_places = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class FoodNutrientAmount(models.Model):
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    nutrient_value = models.FloatField()
    standard_error = models.FloatField(null=True, blank=True)
    number_of_observations = models.FloatField(null=True, blank=True)
    nutrient_source_id = models.IntegerField(null=True, blank=True)
    nutrient_date_of_entry = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('food', 'nutrient')

    def __str__(self):
        return f"{self.food.description} - {self.nutrient.name}: {self.nutrient_value}"
