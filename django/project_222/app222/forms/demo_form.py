from django import forms
from typing import Any

class DemoForm(forms.Form):
    name = forms.CharField(
        label="Ім'я",
        required=True,
        min_length=2,
        max_length=16,
        error_messages={
            'required': "Необхідно зазначити ваше ім'я",
            'min_length': "Введене ім'я закоротке: має бути принаймні 2 літери",
            'max_length': "Введене ім'я задовге: обмежтесь 16 літерами",
        }
    )

    surname = forms.CharField(
        label="Прізвище",
        required=True,
        min_length=2,
        max_length=16,
        error_messages={
            'required': "Необхідно зазначити ваше прізвище",
            'min_length': "Введене прізвище закоротке: має бути принаймні 2 літери",
            'max_length': "Введене прізвище задовге: обмежтесь 16 літерами",
        }
    )

    success_messages = {
        'name': "Ім'я введено коректно",
        'surname': "Прізвище введено коректно"
    }

    def clean(self) -> dict[str, Any]:
        cleaned_values = super().clean()

        def validate_name(value: str, field_name: str):
            parts = value.split('-')

            for part in parts:
                if not part:
                    continue

                # Перша літера велика
                if not part[0].isupper():
                    self.add_error(
                        field_name,
                        forms.ValidationError(
                            f"Перша літера має бути великою у кожній частині ({value})"
                        )
                    )

                # Інші літери маленькі
                if not part[1:].islower():
                    self.add_error(
                        field_name,
                        forms.ValidationError(
                            f"Інші літери мають бути маленькими у кожній частині ({value})"
                        )
                    )

        if 'name' in cleaned_values:
            validate_name(cleaned_values['name'], 'name')

        if 'surname' in cleaned_values:
            validate_name(cleaned_values['surname'], 'surname')

        return cleaned_values