from backend.conftest import fake


def storage_heater_status(db):
    return StorageHeater.objects.create(
        time_stamp=fake.date_time_this_month(),
        relay_one=fake.random_int(min=0, max=1),
        relay_two=fake.random_int(min=0, max=1),
        relay_three=fake.random_int(min=0, max=1),
        relay_four=fake.random_int(min=0, max=1),
        relay_five=fake.random_int(min=0, max=1),
        relay_six=fake.random_int(min=0, max=1),
        temp_one=fake.pyflaot(left_digits=1, right_digits=2,min_value=-55, max_value=120),
        temp_two=fake.pyflaot(left_digits=1, right_digits=2,min_value=-55, max_value=120),
        temp_three=fake.pyflaot(left_digits=1, right_digits=2,min_value=-55, max_value=120),
        temp_four=fake.pyflaot(left_digits=1, right_digits=2,min_value=-55, max_value=120),

    )


def test_storage_heater_status_creation():
    assert isinstance(storage_heater, StorageHeater)


