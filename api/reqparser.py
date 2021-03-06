from flask_restful import reqparse, inputs
from webargs import ValidationError

limit_brightness = 16
limit_x = 11
limit_y = 11
limit_z = 13
limit_face = 6
limit_square = 24
limit_ledstrip = 4
limit_led = 27


def string30(str, type):
    """ fonction to limit test size to 30

    :param str: text
    :param type: use by function
    :return: text if correct
    """
    if len(str) <= 30:
        return str
    raise ValidationError(type + " String must be < 30 len")


def string15(str, type):
    """ fonction to limit test size to 15

    :param str: text
    :param type: use by function
    :return: text if correct
    """
    if len(str) <= 15:
        return str
    raise ValidationError(type + " String must be < 15 len")


def string60(str, type):
    """ fonction to limit test size to 60

    :param str: text
    :param type: use by function
    :return: text if correct
    """
    if len(str) <= 60:
        return str
    raise ValidationError(type + " String must be < 60 len")


parser_change_network = reqparse.RequestParser(bundle_errors=True)
parser_change_network.add_argument('ip1', type=string15, required=True)
parser_change_network.add_argument('ip2', type=string15, required=True)
parser_change_network.add_argument('port1', type=int, choices=range(0, 65536), required=True)
parser_change_network.add_argument('port2', type=int, choices=range(0, 65536), required=True)

parser_change_sequence = reqparse.RequestParser()
parser_change_sequence.add_argument('start', type=inputs.boolean, required=True)

parser_change_fps = reqparse.RequestParser()
parser_change_fps.add_argument('fps', type=int, choices=range(1, 101), required=True)

parser_seq_add = reqparse.RequestParser(bundle_errors=True)
parser_seq_add.add_argument('name', type=string30, required=True)
parser_seq_add.add_argument('code', type=str, required=True)

parser_seq_del = reqparse.RequestParser()
parser_seq_del.add_argument('index', type=int, required=True)

parser_seq_move = reqparse.RequestParser(bundle_errors=True)
parser_seq_move.add_argument('old_index', type=int, required=True)
parser_seq_move.add_argument('new_index', type=int, required=True)

parser_token_find = reqparse.RequestParser()
parser_token_find.add_argument('jti', type=string60, required=True)

parser_token_create = reqparse.RequestParser(bundle_errors=True)
parser_token_create.add_argument('identity', type=string30, required=True)
parser_token_create.add_argument('mode', choices=('user', 'master', 'superuser'),
                                 help="{error_msg}. mode can be user or master", required=True)
parser_token_create.add_argument('date', type=int,
                                 help="{error_msg}. Timestamp error", required=True)

parser_mode = reqparse.RequestParser(bundle_errors=True)
parser_mode.add_argument('mode', choices=('direct', 'sequence'),
                         help="{error_msg}. mode can be direct or sequence", required=True)

parser_cube = reqparse.RequestParser(bundle_errors=True)
parser_cube.add_argument('brightness', type=int, choices=range(limit_brightness),
                         default=15, help="{error_msg}. brightness is between 0 and 15, 15 by default")

parser_face = reqparse.RequestParser(bundle_errors=True)
parser_face.add_argument('idx_face', type=int, choices=range(limit_face),
                         help='{error_msg}. idx_face is between 0 and 5', required=True)
parser_face.add_argument('brightness', type=int, choices=range(limit_brightness),
                         default=15, help="{error_msg}. brightness is between 0 and 15, 15 by default")

parser_square = reqparse.RequestParser(bundle_errors=True)
parser_square.add_argument('idx_face', type=int, choices=range(limit_face),
                           help='{error_msg}. idx_face is between 0 and 5', required=True)
parser_square.add_argument('idx_square', type=int, choices=range(limit_square),
                           help='{error_msg}. idx_square is between 0 and 23', required=True)
parser_square.add_argument('brightness', type=int, choices=range(limit_brightness),
                           default=15, help="{error_msg}. brightness is between 0 and 15, 15 by default")

parser_ledstrip = reqparse.RequestParser(bundle_errors=True)
parser_ledstrip.add_argument('idx_face', type=int, choices=range(limit_face),
                             help='{error_msg}. idx_face is between 0 and 5', required=True)
parser_ledstrip.add_argument('idx_square', type=int, choices=range(limit_square),
                             help='{error_msg}. idx_square is between 0 and 23', required=True)
parser_ledstrip.add_argument('idx_ledstrip', type=int, choices=range(limit_ledstrip),
                             help='{error_msg}. idx_ledstrip is between 0 and 4',
                             required=True)
parser_ledstrip.add_argument('brightness', type=int, choices=range(limit_brightness),
                             default=15, help="{error_msg}. brightness is between 0 and 15, 15 by default")

parser_led = reqparse.RequestParser(bundle_errors=True)
parser_led.add_argument('idx_face', type=int, choices=range(limit_face),
                        help='{error_msg}. idx_face is between 0 and 5', required=True)
parser_led.add_argument('idx_square', type=int, choices=range(limit_square),
                        help='{error_msg}. idx_square is between 0 and 23', required=True)
parser_led.add_argument('idx_ledstrip', type=int, choices=range(limit_ledstrip),
                        help='{error_msg}. idx_ledstrip is between 0 and 4',
                        required=True)
parser_led.add_argument('idx_led', type=int, choices=range(limit_led), help='{error_msg}. idx_led is between 0 and 26',
                        required=True)
parser_led.add_argument('brightness', type=int, choices=range(limit_brightness),
                        default=15, help="{error_msg}. brightness is between 0 and 15, 15 by default")

parser_xyz = reqparse.RequestParser(bundle_errors=True)
parser_xyz.add_argument('idx_x', type=int, choices=range(limit_x), help='{error_msg}. idx_x is between 0 and 10',
                        required=True)
parser_xyz.add_argument('idx_y', type=int, choices=range(limit_y), help='{error_msg}. idx_y is between 0 and 10',
                        required=True)
parser_xyz.add_argument('idx_z', type=int, choices=range(limit_z), help='{error_msg}. idx_z is between 0 and 12',
                        required=True)
parser_xyz.add_argument('brightness', type=int, choices=range(limit_brightness),
                        default=15, help="{error_msg}. brightness is between 0 and 15, 15 by default")

parser_xyz_led = reqparse.RequestParser(bundle_errors=True)
parser_xyz_led.add_argument('idx_x', type=int, choices=range(limit_x), help='{error_msg}. idx_x is between 0 and 10',
                            required=True)
parser_xyz_led.add_argument('idx_y', type=int, choices=range(limit_y), help='{error_msg}. idx_y is between 0 and 10',
                            required=True)
parser_xyz_led.add_argument('idx_z', type=int, choices=range(limit_z), help='{error_msg}. idx_z is between 0 and 12',
                            required=True)
parser_xyz_led.add_argument('idx_led', type=int, choices=range(limit_led),
                            help='{error_msg}. idx_led is between 0 and 26',
                            required=True)
parser_xyz_led.add_argument('brightness', type=int, choices=range(limit_brightness),
                            default=15, help="{error_msg}. brightness is between 0 and 15, 15 by default")
