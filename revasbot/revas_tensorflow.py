import tensorflow as tf
from revasbot.revas_console import RevasConsole as console

console.debug(
    f'Num GPUs Available: {len(tf.config.list_physical_devices("GPU"))}'
)
