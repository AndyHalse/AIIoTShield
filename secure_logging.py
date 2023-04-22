from logging_setup import get_logger

logger = get_logger(__name__)

from cryptography.fernet import Fernet


def setup_secure_logging(log_file, encryption_key):
    """

    :param log_file:
    :param encryption_key:
    :return:
    """
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    logger = logging.getLogger("IoTShield")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    return logger, Fernet(encryption_key)


def log_encrypted(logger, fernet_instance, message):
    """

    :param logger:
    :param fernet_instance:
    :param message:
    """
    encrypted_message = fernet_instance.encrypt(message.encode()).decode()
    logger.debug(encrypted_message)


def decrypt_logs(log_file, encryption_key, output_file):
    """

    :param log_file:
    :param encryption_key:
    :param output_file:
    """
    fernet_instance = Fernet(encryption_key)
    with open(log_file, "r") as log:
        lines = log.readlines()

    decrypted_lines = []
    for line in lines:
        message = line.rstrip().split(" - ")[-1]
        decrypted_message = fernet_instance.decrypt(message.encode()).decode()
        decrypted_line = line.replace(message, decrypted_message)
        decrypted_lines.append(decrypted_line)

    with open(output_file, "w") as decrypted_log:
        decrypted_log.writelines(decrypted_lines)

# Example usage:
# encryption_key = Fernet.generate_key()
# logger, fernet_instance = setup_secure_logging("secure_log.log", encryption_key)
# log_encrypted(logger, fernet_instance, "This is an encrypted log message")
# decrypt_logs("secure_log.log", encryption_key, "decrypted_log.log")
