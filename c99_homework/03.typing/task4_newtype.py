# создать тип Email, и проверку, что адрес содержит @.
# написать функцию send_email, которая принимает валидный Email

if __name__ == "__main__":
    send_email(validate_email("user@example.com"))  # ОК
    send_email("user@example.com")  # mypy должен ругаться на строку, но в runtime все ОК
    send_email("user-example.com")  # mypy должен ругаться на строку, но в runtime все ОК
