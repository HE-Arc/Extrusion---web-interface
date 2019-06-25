from flask_restful import reqparse
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
    if len(str) < 30:
        return str
    raise ValidationError(type + " String must be < 30 len")


parser_token_delete = reqparse.RequestParser()
parser_token_delete.add_argument('identity', type=string30, required=True)

parser_token_create = reqparse.RequestParser()
parser_token_create.add_argument('identity', type=string30, required=True)
parser_token_create.add_argument('mode', choices=('user', 'master'),
                                 help="{error_msg}. mode can be user or master", required=True)
parser_token_create.add_argument('date', type=string30,
                                 help="{error_msg}. Timestamp error", required=True)

parser_mode = reqparse.RequestParser()
parser_mode.add_argument('mode', choices=('user', 'master'),
                         help="{error_msg}. mode can be user or master", required=True)

parser_cube = reqparse.RequestParser()
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
