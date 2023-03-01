from space import Space
from roomtype import RoomType
import pygame
import constants


class Board:
    def __init__(self, window):
        # Map of room -> ids of entrances
        self.entrances = {'Ballroom': [128, 135, 177, 182], 'Billiard Room': [234, 310], 'Conservatory': [139],
                          'Dining Room': [295, 366], 'Hall': [443, 444, 494], 'Kitchen': [148],
                          'Library': [356, 401], 'Lounge': [462], 'Study': [521]}

        # Set player positions to display them in the room
        self.room_display = {'Ballroom': [154, 157, 82, 85, 105, 110],
                             'Billiard Room': [235, 237, 263, 283, 285, 308],
                             'Conservatory': [141, 91, 119, 43, 46, 21],
                             'Dining Room': [246, 244, 241, 318, 316, 313],
                             'Hall': [465, 470, 513, 518, 561, 566],
                             'Kitchen': [100, 97, 26, 28, 146, 3],
                             'Library': [378, 380, 382, 426, 428, 430],
                             'Lounge': [486, 483, 480, 534, 531, 528],
                             'Study': [545, 523, 526, 551, 571, 574]}

        # Keeps track of how many players have occupied the room
        self.room_occupied = {'Ballroom': [False, False, False, False, False, False],
                              'Billiard Room': [False, False, False, False, False, False],
                              'Conservatory': [False, False, False, False, False, False],
                              'Dining Room': [False, False, False, False, False, False],
                              'Hall': [False, False, False, False, False, False],
                              'Kitchen': [False, False, False, False, False, False],
                              'Library': [False, False, False, False, False, False],
                              'Lounge': [False, False, False, False, False, False],
                              'Study': [False, False, False, False, False, False]}

        # The map of the board itself
        self.board = []
        self.window = window
        self.board_mapping = {}

        self.create_board()
        self.draw_board()

    def create_board(self):
        # Create the 25 x 24 space board
        # Row 0
        self.board.append(Space(0, False, RoomType.KITCHEN))
        self.board.append(Space(1, False, RoomType.KITCHEN))
        self.board.append(Space(2, False, RoomType.KITCHEN))
        self.board.append(Space(3, False, RoomType.KITCHEN))
        self.board.append(Space(4, False, RoomType.KITCHEN))
        self.board.append(Space(5, False, RoomType.KITCHEN))
        self.board.append(Space(6, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(7, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(8, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(9, False, RoomType.START))
        self.board.append(Space(10, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(11, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(12, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(13, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(14, False, RoomType.START))
        self.board.append(Space(15, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(16, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(17, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(18, False, RoomType.CONSERVATORY))
        self.board.append(Space(19, False, RoomType.CONSERVATORY))
        self.board.append(Space(20, False, RoomType.CONSERVATORY))
        self.board.append(Space(21, False, RoomType.CONSERVATORY))
        self.board.append(Space(22, False, RoomType.CONSERVATORY))
        self.board.append(Space(23, False, RoomType.CONSERVATORY))

        # Row 1
        self.board.append(Space(24, False, RoomType.KITCHEN))
        self.board.append(Space(25, False, RoomType.KITCHEN))
        self.board.append(Space(26, False, RoomType.KITCHEN))
        self.board.append(Space(27, False, RoomType.KITCHEN))
        self.board.append(Space(28, False, RoomType.KITCHEN))
        self.board.append(Space(29, False, RoomType.KITCHEN))
        self.board.append(Space(30, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(31, False, RoomType.HALLWAY))
        self.board.append(Space(32, False, RoomType.HALLWAY))
        self.board.append(Space(33, False, RoomType.HALLWAY))
        self.board.append(Space(34, False, RoomType.BALL))
        self.board.append(Space(35, False, RoomType.BALL))
        self.board.append(Space(36, False, RoomType.BALL))
        self.board.append(Space(37, False, RoomType.BALL))
        self.board.append(Space(38, False, RoomType.HALLWAY))
        self.board.append(Space(39, False, RoomType.HALLWAY))
        self.board.append(Space(40, False, RoomType.HALLWAY))
        self.board.append(Space(41, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(42, False, RoomType.CONSERVATORY))
        self.board.append(Space(43, False, RoomType.CONSERVATORY))
        self.board.append(Space(44, False, RoomType.CONSERVATORY))
        self.board.append(Space(45, False, RoomType.CONSERVATORY))
        self.board.append(Space(56, False, RoomType.CONSERVATORY))
        self.board.append(Space(47, False, RoomType.CONSERVATORY))

        # Row 2
        self.board.append(Space(48, False, RoomType.KITCHEN))
        self.board.append(Space(49, False, RoomType.KITCHEN))
        self.board.append(Space(50, False, RoomType.KITCHEN))
        self.board.append(Space(51, False, RoomType.KITCHEN))
        self.board.append(Space(52, False, RoomType.KITCHEN))
        self.board.append(Space(53, False, RoomType.KITCHEN))
        self.board.append(Space(54, False, RoomType.HALLWAY))
        self.board.append(Space(55, False, RoomType.HALLWAY))
        self.board.append(Space(56, False, RoomType.BALL))
        self.board.append(Space(57, False, RoomType.BALL))
        self.board.append(Space(58, False, RoomType.BALL))
        self.board.append(Space(59, False, RoomType.BALL))
        self.board.append(Space(60, False, RoomType.BALL))
        self.board.append(Space(61, False, RoomType.BALL))
        self.board.append(Space(62, False, RoomType.BALL))
        self.board.append(Space(63, False, RoomType.BALL))
        self.board.append(Space(64, False, RoomType.HALLWAY))
        self.board.append(Space(65, False, RoomType.HALLWAY))
        self.board.append(Space(66, False, RoomType.CONSERVATORY))
        self.board.append(Space(67, False, RoomType.CONSERVATORY))
        self.board.append(Space(68, False, RoomType.CONSERVATORY))
        self.board.append(Space(69, False, RoomType.CONSERVATORY))
        self.board.append(Space(70, False, RoomType.CONSERVATORY))
        self.board.append(Space(71, False, RoomType.CONSERVATORY))

        # Row 3
        self.board.append(Space(72, False, RoomType.KITCHEN))
        self.board.append(Space(73, False, RoomType.KITCHEN))
        self.board.append(Space(74, False, RoomType.KITCHEN))
        self.board.append(Space(75, False, RoomType.KITCHEN))
        self.board.append(Space(76, False, RoomType.KITCHEN))
        self.board.append(Space(77, False, RoomType.KITCHEN))
        self.board.append(Space(78, False, RoomType.HALLWAY))
        self.board.append(Space(79, False, RoomType.HALLWAY))
        self.board.append(Space(80, False, RoomType.BALL))
        self.board.append(Space(81, False, RoomType.BALL))
        self.board.append(Space(82, False, RoomType.BALL))
        self.board.append(Space(83, False, RoomType.BALL))
        self.board.append(Space(84, False, RoomType.BALL))
        self.board.append(Space(85, False, RoomType.BALL))
        self.board.append(Space(86, False, RoomType.BALL))
        self.board.append(Space(87, False, RoomType.BALL))
        self.board.append(Space(88, False, RoomType.HALLWAY))
        self.board.append(Space(89, False, RoomType.HALLWAY))
        self.board.append(Space(90, False, RoomType.CONSERVATORY))
        self.board.append(Space(91, False, RoomType.CONSERVATORY))
        self.board.append(Space(92, False, RoomType.CONSERVATORY))
        self.board.append(Space(93, False, RoomType.CONSERVATORY))
        self.board.append(Space(94, False, RoomType.CONSERVATORY))
        self.board.append(Space(95, False, RoomType.CONSERVATORY))

        # Row 4
        self.board.append(Space(96, False, RoomType.KITCHEN))
        self.board.append(Space(97, False, RoomType.KITCHEN))
        self.board.append(Space(98, False, RoomType.KITCHEN))
        self.board.append(Space(99, False, RoomType.KITCHEN))
        self.board.append(Space(100, False, RoomType.KITCHEN))
        self.board.append(Space(101, False, RoomType.KITCHEN))
        self.board.append(Space(102, False, RoomType.HALLWAY))
        self.board.append(Space(103, False, RoomType.HALLWAY))
        self.board.append(Space(104, False, RoomType.BALL))
        self.board.append(Space(105, False, RoomType.BALL))
        self.board.append(Space(106, False, RoomType.BALL))
        self.board.append(Space(107, False, RoomType.BALL))
        self.board.append(Space(108, False, RoomType.BALL))
        self.board.append(Space(109, False, RoomType.BALL))
        self.board.append(Space(110, False, RoomType.BALL))
        self.board.append(Space(111, False, RoomType.BALL))
        self.board.append(Space(112, False, RoomType.HALLWAY))
        self.board.append(Space(113, False, RoomType.HALLWAY))
        self.board.append(Space(114, False, RoomType.CONSERVATORY))
        self.board.append(Space(115, False, RoomType.CONSERVATORY))
        self.board.append(Space(116, False, RoomType.CONSERVATORY))
        self.board.append(Space(117, False, RoomType.CONSERVATORY))
        self.board.append(Space(118, False, RoomType.CONSERVATORY))
        self.board.append(Space(119, False, RoomType.CONSERVATORY))

        # Row 5
        self.board.append(Space(120, False, RoomType.KITCHEN))
        self.board.append(Space(121, False, RoomType.KITCHEN))
        self.board.append(Space(122, False, RoomType.KITCHEN))
        self.board.append(Space(123, False, RoomType.KITCHEN))
        self.board.append(Space(124, False, RoomType.KITCHEN))
        self.board.append(Space(125, False, RoomType.KITCHEN))
        self.board.append(Space(126, False, RoomType.HALLWAY))
        self.board.append(Space(127, False, RoomType.HALLWAY))
        self.board.append(Space(128, False, RoomType.BALL))
        self.board.append(Space(129, False, RoomType.BALL))
        self.board.append(Space(130, False, RoomType.BALL))
        self.board.append(Space(131, False, RoomType.BALL))
        self.board.append(Space(132, False, RoomType.BALL))
        self.board.append(Space(133, False, RoomType.BALL))
        self.board.append(Space(134, False, RoomType.BALL))
        self.board.append(Space(135, False, RoomType.BALL))
        self.board.append(Space(136, False, RoomType.HALLWAY))
        self.board.append(Space(137, False, RoomType.HALLWAY))
        self.board.append(Space(138, False, RoomType.HALLWAY))
        self.board.append(Space(139, False, RoomType.CONSERVATORY))
        self.board.append(Space(140, False, RoomType.CONSERVATORY))
        self.board.append(Space(141, False, RoomType.CONSERVATORY))
        self.board.append(Space(142, False, RoomType.CONSERVATORY))
        self.board.append(Space(143, False, RoomType.OUT_OF_BOUNDS))

        # Row 6
        self.board.append(Space(144, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(145, False, RoomType.KITCHEN))
        self.board.append(Space(146, False, RoomType.KITCHEN))
        self.board.append(Space(147, False, RoomType.KITCHEN))
        self.board.append(Space(148, False, RoomType.KITCHEN))
        self.board.append(Space(149, False, RoomType.KITCHEN))
        self.board.append(Space(150, False, RoomType.HALLWAY))
        self.board.append(Space(151, False, RoomType.HALLWAY))
        self.board.append(Space(152, False, RoomType.BALL))
        self.board.append(Space(153, False, RoomType.BALL))
        self.board.append(Space(154, False, RoomType.BALL))
        self.board.append(Space(155, False, RoomType.BALL))
        self.board.append(Space(156, False, RoomType.BALL))
        self.board.append(Space(157, False, RoomType.BALL))
        self.board.append(Space(158, False, RoomType.BALL))
        self.board.append(Space(159, False, RoomType.BALL))
        self.board.append(Space(160, False, RoomType.HALLWAY))
        self.board.append(Space(161, False, RoomType.HALLWAY))
        self.board.append(Space(162, False, RoomType.HALLWAY))
        self.board.append(Space(163, False, RoomType.HALLWAY))
        self.board.append(Space(164, False, RoomType.HALLWAY))
        self.board.append(Space(165, False, RoomType.HALLWAY))
        self.board.append(Space(166, False, RoomType.HALLWAY))
        self.board.append(Space(167, False, RoomType.START))

        # Row 7
        self.board.append(Space(168, False, RoomType.HALLWAY))
        self.board.append(Space(169, False, RoomType.HALLWAY))
        self.board.append(Space(170, False, RoomType.HALLWAY))
        self.board.append(Space(171, False, RoomType.HALLWAY))
        self.board.append(Space(172, False, RoomType.HALLWAY))
        self.board.append(Space(173, False, RoomType.HALLWAY))
        self.board.append(Space(174, False, RoomType.HALLWAY))
        self.board.append(Space(175, False, RoomType.HALLWAY))
        self.board.append(Space(176, False, RoomType.BALL))
        self.board.append(Space(177, False, RoomType.BALL))
        self.board.append(Space(178, False, RoomType.BALL))
        self.board.append(Space(179, False, RoomType.BALL))
        self.board.append(Space(180, False, RoomType.BALL))
        self.board.append(Space(181, False, RoomType.BALL))
        self.board.append(Space(182, False, RoomType.BALL))
        self.board.append(Space(183, False, RoomType.BALL))
        self.board.append(Space(184, False, RoomType.HALLWAY))
        self.board.append(Space(185, False, RoomType.HALLWAY))
        self.board.append(Space(186, False, RoomType.HALLWAY))
        self.board.append(Space(187, False, RoomType.HALLWAY))
        self.board.append(Space(188, False, RoomType.HALLWAY))
        self.board.append(Space(189, False, RoomType.HALLWAY))
        self.board.append(Space(190, False, RoomType.HALLWAY))
        self.board.append(Space(191, False, RoomType.OUT_OF_BOUNDS))

        # Row 8
        self.board.append(Space(192, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(193, False, RoomType.HALLWAY))
        self.board.append(Space(194, False, RoomType.HALLWAY))
        self.board.append(Space(195, False, RoomType.HALLWAY))
        self.board.append(Space(196, False, RoomType.HALLWAY))
        self.board.append(Space(197, False, RoomType.HALLWAY))
        self.board.append(Space(198, False, RoomType.HALLWAY))
        self.board.append(Space(199, False, RoomType.HALLWAY))
        self.board.append(Space(200, False, RoomType.HALLWAY))
        self.board.append(Space(201, False, RoomType.HALLWAY))
        self.board.append(Space(202, False, RoomType.HALLWAY))
        self.board.append(Space(203, False, RoomType.HALLWAY))
        self.board.append(Space(204, False, RoomType.HALLWAY))
        self.board.append(Space(205, False, RoomType.HALLWAY))
        self.board.append(Space(206, False, RoomType.HALLWAY))
        self.board.append(Space(207, False, RoomType.HALLWAY))
        self.board.append(Space(208, False, RoomType.HALLWAY))
        self.board.append(Space(209, False, RoomType.HALLWAY))
        self.board.append(Space(210, False, RoomType.BILLIARD))
        self.board.append(Space(211, False, RoomType.BILLIARD))
        self.board.append(Space(212, False, RoomType.BILLIARD))
        self.board.append(Space(213, False, RoomType.BILLIARD))
        self.board.append(Space(214, False, RoomType.BILLIARD))
        self.board.append(Space(215, False, RoomType.BILLIARD))

        # Row 9
        self.board.append(Space(216, False, RoomType.DINING))
        self.board.append(Space(217, False, RoomType.DINING))
        self.board.append(Space(218, False, RoomType.DINING))
        self.board.append(Space(219, False, RoomType.DINING))
        self.board.append(Space(220, False, RoomType.DINING))
        self.board.append(Space(221, False, RoomType.HALLWAY))
        self.board.append(Space(222, False, RoomType.HALLWAY))
        self.board.append(Space(223, False, RoomType.HALLWAY))
        self.board.append(Space(224, False, RoomType.HALLWAY))
        self.board.append(Space(225, False, RoomType.HALLWAY))
        self.board.append(Space(226, False, RoomType.HALLWAY))
        self.board.append(Space(227, False, RoomType.HALLWAY))
        self.board.append(Space(228, False, RoomType.HALLWAY))
        self.board.append(Space(229, False, RoomType.HALLWAY))
        self.board.append(Space(230, False, RoomType.HALLWAY))
        self.board.append(Space(231, False, RoomType.HALLWAY))
        self.board.append(Space(232, False, RoomType.HALLWAY))
        self.board.append(Space(233, False, RoomType.HALLWAY))
        self.board.append(Space(234, False, RoomType.BILLIARD))
        self.board.append(Space(235, False, RoomType.BILLIARD))
        self.board.append(Space(236, False, RoomType.BILLIARD))
        self.board.append(Space(237, False, RoomType.BILLIARD))
        self.board.append(Space(238, False, RoomType.BILLIARD))
        self.board.append(Space(239, False, RoomType.BILLIARD))

        # Row 10
        self.board.append(Space(240, False, RoomType.DINING))
        self.board.append(Space(241, False, RoomType.DINING))
        self.board.append(Space(242, False, RoomType.DINING))
        self.board.append(Space(243, False, RoomType.DINING))
        self.board.append(Space(244, False, RoomType.DINING))
        self.board.append(Space(245, False, RoomType.DINING))
        self.board.append(Space(246, False, RoomType.DINING))
        self.board.append(Space(247, False, RoomType.DINING))
        self.board.append(Space(248, False, RoomType.HALLWAY))
        self.board.append(Space(249, False, RoomType.HALLWAY))
        self.board.append(Space(250, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(251, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(252, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(253, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(254, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(255, False, RoomType.HALLWAY))
        self.board.append(Space(256, False, RoomType.HALLWAY))
        self.board.append(Space(257, False, RoomType.HALLWAY))
        self.board.append(Space(258, False, RoomType.BILLIARD))
        self.board.append(Space(259, False, RoomType.BILLIARD))
        self.board.append(Space(260, False, RoomType.BILLIARD))
        self.board.append(Space(261, False, RoomType.BILLIARD))
        self.board.append(Space(262, False, RoomType.BILLIARD))
        self.board.append(Space(263, False, RoomType.BILLIARD))

        # Row 11
        self.board.append(Space(264, False, RoomType.DINING))
        self.board.append(Space(265, False, RoomType.DINING))
        self.board.append(Space(266, False, RoomType.DINING))
        self.board.append(Space(267, False, RoomType.DINING))
        self.board.append(Space(268, False, RoomType.DINING))
        self.board.append(Space(269, False, RoomType.DINING))
        self.board.append(Space(270, False, RoomType.DINING))
        self.board.append(Space(271, False, RoomType.DINING))
        self.board.append(Space(272, False, RoomType.HALLWAY))
        self.board.append(Space(273, False, RoomType.HALLWAY))
        self.board.append(Space(274, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(275, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(276, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(277, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(278, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(279, False, RoomType.HALLWAY))
        self.board.append(Space(280, False, RoomType.HALLWAY))
        self.board.append(Space(281, False, RoomType.HALLWAY))
        self.board.append(Space(282, False, RoomType.BILLIARD))
        self.board.append(Space(283, False, RoomType.BILLIARD))
        self.board.append(Space(284, False, RoomType.BILLIARD))
        self.board.append(Space(285, False, RoomType.BILLIARD))
        self.board.append(Space(286, False, RoomType.BILLIARD))
        self.board.append(Space(287, False, RoomType.BILLIARD))

        # Row 12
        self.board.append(Space(288, False, RoomType.DINING))
        self.board.append(Space(289, False, RoomType.DINING))
        self.board.append(Space(290, False, RoomType.DINING))
        self.board.append(Space(291, False, RoomType.DINING))
        self.board.append(Space(292, False, RoomType.DINING))
        self.board.append(Space(293, False, RoomType.DINING))
        self.board.append(Space(294, False, RoomType.DINING))
        self.board.append(Space(295, False, RoomType.DINING))
        self.board.append(Space(296, False, RoomType.HALLWAY))
        self.board.append(Space(297, False, RoomType.HALLWAY))
        self.board.append(Space(298, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(299, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(300, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(301, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(302, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(303, False, RoomType.HALLWAY))
        self.board.append(Space(304, False, RoomType.HALLWAY))
        self.board.append(Space(305, False, RoomType.HALLWAY))
        self.board.append(Space(306, False, RoomType.BILLIARD))
        self.board.append(Space(307, False, RoomType.BILLIARD))
        self.board.append(Space(308, False, RoomType.BILLIARD))
        self.board.append(Space(309, False, RoomType.BILLIARD))
        self.board.append(Space(310, False, RoomType.BILLIARD))
        self.board.append(Space(311, False, RoomType.BILLIARD))

        # Row 13
        self.board.append(Space(312, False, RoomType.DINING))
        self.board.append(Space(313, False, RoomType.DINING))
        self.board.append(Space(314, False, RoomType.DINING))
        self.board.append(Space(315, False, RoomType.DINING))
        self.board.append(Space(316, False, RoomType.DINING))
        self.board.append(Space(317, False, RoomType.DINING))
        self.board.append(Space(318, False, RoomType.DINING))
        self.board.append(Space(319, False, RoomType.DINING))
        self.board.append(Space(320, False, RoomType.HALLWAY))
        self.board.append(Space(321, False, RoomType.HALLWAY))
        self.board.append(Space(322, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(323, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(324, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(325, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(326, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(327, False, RoomType.HALLWAY))
        self.board.append(Space(328, False, RoomType.HALLWAY))
        self.board.append(Space(329, False, RoomType.HALLWAY))
        self.board.append(Space(330, False, RoomType.HALLWAY))
        self.board.append(Space(331, False, RoomType.HALLWAY))
        self.board.append(Space(332, False, RoomType.HALLWAY))
        self.board.append(Space(333, False, RoomType.HALLWAY))
        self.board.append(Space(334, False, RoomType.HALLWAY))
        self.board.append(Space(335, False, RoomType.OUT_OF_BOUNDS))

        # Row 14
        self.board.append(Space(336, False, RoomType.DINING))
        self.board.append(Space(337, False, RoomType.DINING))
        self.board.append(Space(338, False, RoomType.DINING))
        self.board.append(Space(339, False, RoomType.DINING))
        self.board.append(Space(340, False, RoomType.DINING))
        self.board.append(Space(341, False, RoomType.DINING))
        self.board.append(Space(342, False, RoomType.DINING))
        self.board.append(Space(343, False, RoomType.DINING))
        self.board.append(Space(344, False, RoomType.HALLWAY))
        self.board.append(Space(345, False, RoomType.HALLWAY))
        self.board.append(Space(346, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(347, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(348, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(349, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(350, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(351, False, RoomType.HALLWAY))
        self.board.append(Space(352, False, RoomType.HALLWAY))
        self.board.append(Space(353, False, RoomType.HALLWAY))
        self.board.append(Space(354, False, RoomType.LIBRARY))
        self.board.append(Space(355, False, RoomType.LIBRARY))
        self.board.append(Space(356, False, RoomType.LIBRARY))
        self.board.append(Space(357, False, RoomType.LIBRARY))
        self.board.append(Space(358, False, RoomType.LIBRARY))
        self.board.append(Space(359, False, RoomType.OUT_OF_BOUNDS))

        # Row 15
        self.board.append(Space(360, False, RoomType.DINING))
        self.board.append(Space(361, False, RoomType.DINING))
        self.board.append(Space(362, False, RoomType.DINING))
        self.board.append(Space(363, False, RoomType.DINING))
        self.board.append(Space(364, False, RoomType.DINING))
        self.board.append(Space(365, False, RoomType.DINING))
        self.board.append(Space(366, False, RoomType.DINING))
        self.board.append(Space(367, False, RoomType.DINING))
        self.board.append(Space(368, False, RoomType.HALLWAY))
        self.board.append(Space(369, False, RoomType.HALLWAY))
        self.board.append(Space(370, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(371, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(372, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(373, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(374, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(375, False, RoomType.HALLWAY))
        self.board.append(Space(376, False, RoomType.HALLWAY))
        self.board.append(Space(377, False, RoomType.LIBRARY))
        self.board.append(Space(378, False, RoomType.LIBRARY))
        self.board.append(Space(379, False, RoomType.LIBRARY))
        self.board.append(Space(380, False, RoomType.LIBRARY))
        self.board.append(Space(381, False, RoomType.LIBRARY))
        self.board.append(Space(382, False, RoomType.LIBRARY))
        self.board.append(Space(383, False, RoomType.LIBRARY))

        # Row 16
        self.board.append(Space(384, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(385, False, RoomType.HALLWAY))
        self.board.append(Space(386, False, RoomType.HALLWAY))
        self.board.append(Space(387, False, RoomType.HALLWAY))
        self.board.append(Space(388, False, RoomType.HALLWAY))
        self.board.append(Space(389, False, RoomType.HALLWAY))
        self.board.append(Space(390, False, RoomType.HALLWAY))
        self.board.append(Space(391, False, RoomType.HALLWAY))
        self.board.append(Space(392, False, RoomType.HALLWAY))
        self.board.append(Space(393, False, RoomType.HALLWAY))
        self.board.append(Space(394, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(395, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(396, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(397, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(398, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(399, False, RoomType.HALLWAY))
        self.board.append(Space(400, False, RoomType.HALLWAY))
        self.board.append(Space(401, False, RoomType.LIBRARY))
        self.board.append(Space(402, False, RoomType.LIBRARY))
        self.board.append(Space(403, False, RoomType.LIBRARY))
        self.board.append(Space(404, False, RoomType.LIBRARY))
        self.board.append(Space(405, False, RoomType.LIBRARY))
        self.board.append(Space(406, False, RoomType.LIBRARY))
        self.board.append(Space(407, False, RoomType.LIBRARY))

        # Row 17
        self.board.append(Space(408, False, RoomType.START))
        self.board.append(Space(409, False, RoomType.HALLWAY))
        self.board.append(Space(410, False, RoomType.HALLWAY))
        self.board.append(Space(411, False, RoomType.HALLWAY))
        self.board.append(Space(412, False, RoomType.HALLWAY))
        self.board.append(Space(413, False, RoomType.HALLWAY))
        self.board.append(Space(414, False, RoomType.HALLWAY))
        self.board.append(Space(415, False, RoomType.HALLWAY))
        self.board.append(Space(416, False, RoomType.HALLWAY))
        self.board.append(Space(417, False, RoomType.HALLWAY))
        self.board.append(Space(418, False, RoomType.HALLWAY))
        self.board.append(Space(419, False, RoomType.HALLWAY))
        self.board.append(Space(420, False, RoomType.HALLWAY))
        self.board.append(Space(421, False, RoomType.HALLWAY))
        self.board.append(Space(422, False, RoomType.HALLWAY))
        self.board.append(Space(423, False, RoomType.HALLWAY))
        self.board.append(Space(424, False, RoomType.HALLWAY))
        self.board.append(Space(425, False, RoomType.LIBRARY))
        self.board.append(Space(426, False, RoomType.LIBRARY))
        self.board.append(Space(427, False, RoomType.LIBRARY))
        self.board.append(Space(428, False, RoomType.LIBRARY))
        self.board.append(Space(429, False, RoomType.LIBRARY))
        self.board.append(Space(430, False, RoomType.LIBRARY))
        self.board.append(Space(431, False, RoomType.LIBRARY))

        # Row 18
        self.board.append(Space(432, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(433, False, RoomType.HALLWAY))
        self.board.append(Space(434, False, RoomType.HALLWAY))
        self.board.append(Space(435, False, RoomType.HALLWAY))
        self.board.append(Space(436, False, RoomType.HALLWAY))
        self.board.append(Space(437, False, RoomType.HALLWAY))
        self.board.append(Space(438, False, RoomType.HALLWAY))
        self.board.append(Space(439, False, RoomType.HALLWAY))
        self.board.append(Space(440, False, RoomType.HALLWAY))
        self.board.append(Space(441, False, RoomType.HALL))
        self.board.append(Space(442, False, RoomType.HALL))
        self.board.append(Space(443, False, RoomType.HALL))
        self.board.append(Space(444, False, RoomType.HALL))
        self.board.append(Space(445, False, RoomType.HALL))
        self.board.append(Space(446, False, RoomType.HALL))
        self.board.append(Space(447, False, RoomType.HALLWAY))
        self.board.append(Space(448, False, RoomType.HALLWAY))
        self.board.append(Space(449, False, RoomType.HALLWAY))
        self.board.append(Space(450, False, RoomType.LIBRARY))
        self.board.append(Space(451, False, RoomType.LIBRARY))
        self.board.append(Space(452, False, RoomType.LIBRARY))
        self.board.append(Space(453, False, RoomType.LIBRARY))
        self.board.append(Space(454, False, RoomType.LIBRARY))
        self.board.append(Space(455, False, RoomType.OUT_OF_BOUNDS))

        # Row 19
        self.board.append(Space(456, False, RoomType.LOUNGE))
        self.board.append(Space(457, False, RoomType.LOUNGE))
        self.board.append(Space(458, False, RoomType.LOUNGE))
        self.board.append(Space(459, False, RoomType.LOUNGE))
        self.board.append(Space(460, False, RoomType.LOUNGE))
        self.board.append(Space(461, False, RoomType.LOUNGE))
        self.board.append(Space(462, False, RoomType.LOUNGE))
        self.board.append(Space(463, False, RoomType.HALLWAY))
        self.board.append(Space(464, False, RoomType.HALLWAY))
        self.board.append(Space(465, False, RoomType.HALL))
        self.board.append(Space(466, False, RoomType.HALL))
        self.board.append(Space(467, False, RoomType.HALL))
        self.board.append(Space(468, False, RoomType.HALL))
        self.board.append(Space(469, False, RoomType.HALL))
        self.board.append(Space(470, False, RoomType.HALL))
        self.board.append(Space(471, False, RoomType.HALLWAY))
        self.board.append(Space(472, False, RoomType.HALLWAY))
        self.board.append(Space(473, False, RoomType.HALLWAY))
        self.board.append(Space(474, False, RoomType.HALLWAY))
        self.board.append(Space(475, False, RoomType.HALLWAY))
        self.board.append(Space(476, False, RoomType.HALLWAY))
        self.board.append(Space(477, False, RoomType.HALLWAY))
        self.board.append(Space(478, False, RoomType.HALLWAY))
        self.board.append(Space(479, False, RoomType.START))

        # Row 20
        self.board.append(Space(480, False, RoomType.LOUNGE))
        self.board.append(Space(481, False, RoomType.LOUNGE))
        self.board.append(Space(482, False, RoomType.LOUNGE))
        self.board.append(Space(483, False, RoomType.LOUNGE))
        self.board.append(Space(484, False, RoomType.LOUNGE))
        self.board.append(Space(485, False, RoomType.LOUNGE))
        self.board.append(Space(486, False, RoomType.LOUNGE))
        self.board.append(Space(487, False, RoomType.HALLWAY))
        self.board.append(Space(488, False, RoomType.HALLWAY))
        self.board.append(Space(489, False, RoomType.HALL))
        self.board.append(Space(490, False, RoomType.HALL))
        self.board.append(Space(491, False, RoomType.HALL))
        self.board.append(Space(492, False, RoomType.HALL))
        self.board.append(Space(493, False, RoomType.HALL))
        self.board.append(Space(494, False, RoomType.HALL))
        self.board.append(Space(495, False, RoomType.HALLWAY))
        self.board.append(Space(496, False, RoomType.HALLWAY))
        self.board.append(Space(497, False, RoomType.HALLWAY))
        self.board.append(Space(498, False, RoomType.HALLWAY))
        self.board.append(Space(499, False, RoomType.HALLWAY))
        self.board.append(Space(500, False, RoomType.HALLWAY))
        self.board.append(Space(501, False, RoomType.HALLWAY))
        self.board.append(Space(502, False, RoomType.HALLWAY))
        self.board.append(Space(503, False, RoomType.OUT_OF_BOUNDS))

        # Row 21
        self.board.append(Space(504, False, RoomType.LOUNGE))
        self.board.append(Space(505, False, RoomType.LOUNGE))
        self.board.append(Space(506, False, RoomType.LOUNGE))
        self.board.append(Space(507, False, RoomType.LOUNGE))
        self.board.append(Space(508, False, RoomType.LOUNGE))
        self.board.append(Space(509, False, RoomType.LOUNGE))
        self.board.append(Space(510, False, RoomType.LOUNGE))
        self.board.append(Space(511, False, RoomType.HALLWAY))
        self.board.append(Space(512, False, RoomType.HALLWAY))
        self.board.append(Space(513, False, RoomType.HALL))
        self.board.append(Space(514, False, RoomType.HALL))
        self.board.append(Space(515, False, RoomType.HALL))
        self.board.append(Space(516, False, RoomType.HALL))
        self.board.append(Space(517, False, RoomType.HALL))
        self.board.append(Space(518, False, RoomType.HALL))
        self.board.append(Space(519, False, RoomType.HALLWAY))
        self.board.append(Space(520, False, RoomType.HALLWAY))
        self.board.append(Space(521, False, RoomType.STUDY))
        self.board.append(Space(522, False, RoomType.STUDY))
        self.board.append(Space(523, False, RoomType.STUDY))
        self.board.append(Space(524, False, RoomType.STUDY))
        self.board.append(Space(525, False, RoomType.STUDY))
        self.board.append(Space(526, False, RoomType.STUDY))
        self.board.append(Space(527, False, RoomType.STUDY))

        # Row 22
        self.board.append(Space(528, False, RoomType.LOUNGE))
        self.board.append(Space(529, False, RoomType.LOUNGE))
        self.board.append(Space(530, False, RoomType.LOUNGE))
        self.board.append(Space(531, False, RoomType.LOUNGE))
        self.board.append(Space(532, False, RoomType.LOUNGE))
        self.board.append(Space(533, False, RoomType.LOUNGE))
        self.board.append(Space(534, False, RoomType.LOUNGE))
        self.board.append(Space(535, False, RoomType.HALLWAY))
        self.board.append(Space(536, False, RoomType.HALLWAY))
        self.board.append(Space(537, False, RoomType.HALL))
        self.board.append(Space(538, False, RoomType.HALL))
        self.board.append(Space(539, False, RoomType.HALL))
        self.board.append(Space(540, False, RoomType.HALL))
        self.board.append(Space(541, False, RoomType.HALL))
        self.board.append(Space(542, False, RoomType.HALL))
        self.board.append(Space(543, False, RoomType.HALLWAY))
        self.board.append(Space(544, False, RoomType.HALLWAY))
        self.board.append(Space(545, False, RoomType.STUDY))
        self.board.append(Space(546, False, RoomType.STUDY))
        self.board.append(Space(547, False, RoomType.STUDY))
        self.board.append(Space(548, False, RoomType.STUDY))
        self.board.append(Space(549, False, RoomType.STUDY))
        self.board.append(Space(550, False, RoomType.STUDY))
        self.board.append(Space(551, False, RoomType.STUDY))

        # Row 23
        self.board.append(Space(552, False, RoomType.LOUNGE))
        self.board.append(Space(553, False, RoomType.LOUNGE))
        self.board.append(Space(554, False, RoomType.LOUNGE))
        self.board.append(Space(555, False, RoomType.LOUNGE))
        self.board.append(Space(556, False, RoomType.LOUNGE))
        self.board.append(Space(557, False, RoomType.LOUNGE))
        self.board.append(Space(558, False, RoomType.LOUNGE))
        self.board.append(Space(559, False, RoomType.HALLWAY))
        self.board.append(Space(560, False, RoomType.HALLWAY))
        self.board.append(Space(561, False, RoomType.HALL))
        self.board.append(Space(562, False, RoomType.HALL))
        self.board.append(Space(563, False, RoomType.HALL))
        self.board.append(Space(564, False, RoomType.HALL))
        self.board.append(Space(565, False, RoomType.HALL))
        self.board.append(Space(566, False, RoomType.HALL))
        self.board.append(Space(567, False, RoomType.HALLWAY))
        self.board.append(Space(568, False, RoomType.HALLWAY))
        self.board.append(Space(569, False, RoomType.STUDY))
        self.board.append(Space(570, False, RoomType.STUDY))
        self.board.append(Space(571, False, RoomType.STUDY))
        self.board.append(Space(572, False, RoomType.STUDY))
        self.board.append(Space(573, False, RoomType.STUDY))
        self.board.append(Space(574, False, RoomType.STUDY))
        self.board.append(Space(575, False, RoomType.STUDY))

        # Row 24
        self.board.append(Space(576, False, RoomType.LOUNGE))
        self.board.append(Space(577, False, RoomType.LOUNGE))
        self.board.append(Space(578, False, RoomType.LOUNGE))
        self.board.append(Space(579, False, RoomType.LOUNGE))
        self.board.append(Space(580, False, RoomType.LOUNGE))
        self.board.append(Space(581, False, RoomType.LOUNGE))
        self.board.append(Space(582, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(583, False, RoomType.START))
        self.board.append(Space(584, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(585, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(586, False, RoomType.HALL))
        self.board.append(Space(587, False, RoomType.HALL))
        self.board.append(Space(588, False, RoomType.HALL))
        self.board.append(Space(589, False, RoomType.HALL))
        self.board.append(Space(590, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(591, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(592, False, RoomType.HALLWAY))
        self.board.append(Space(593, False, RoomType.OUT_OF_BOUNDS))
        self.board.append(Space(594, False, RoomType.STUDY))
        self.board.append(Space(595, False, RoomType.STUDY))
        self.board.append(Space(596, False, RoomType.STUDY))
        self.board.append(Space(597, False, RoomType.STUDY))
        self.board.append(Space(598, False, RoomType.STUDY))
        self.board.append(Space(599, False, RoomType.STUDY))

    def print_board(self):
        # 25 rows, 24 columns
        for r in range(0, 25):
            row = ''
            for c in range(0, 24):
                space_id = (r * 24) + c
                space_type = self.board[space_id].get_room()

                if space_type == RoomType.BALL:
                    row += '[B]'
                elif space_type == RoomType.BILLIARD:
                    row += '[I]'
                elif space_type == RoomType.CONSERVATORY:
                    row += '[C]'
                elif space_type == RoomType.DINING:
                    row += '[D]'
                elif space_type == RoomType.HALL:
                    row += '[H]'
                elif space_type == RoomType.HALLWAY:
                    row += '[ ]'
                elif space_type == RoomType.KITCHEN:
                    row += '[K]'
                elif space_type == RoomType.LIBRARY:
                    row += '[L]'
                elif space_type == RoomType.LOUNGE:
                    row += '[O]'
                elif space_type == RoomType.OUT_OF_BOUNDS:
                    row += '[X]'
                elif space_type == RoomType.START:
                    row += '[R]'
                elif space_type == RoomType.STUDY:
                    row += '[S]'

            print(row)

    def draw_board(self):
        # How big to make the spaces
        SQUARE_SIZE = constants.SQUARE_SIZE

        # Define colors
        BACKGROUND = (192, 192, 192)
        HALLWAY = (133, 76, 38)
        ENTRANCES = (192, 192, 192)
        OOB = (0, 0, 0)
        KITCHEN = (232, 167, 155)
        BALL = (196, 245, 199)
        CONSERVATORY = (58, 173, 214)
        DINING = (255, 201, 244)
        BILLIARDS = (217, 222, 151)
        LIBRARY = (240, 169, 98)
        LOUNGE = (191, 173, 204)
        HALL = (118, 194, 174)
        STUDY = (93, 101, 163)

        WHITE = (255, 255, 255)
        MUSTARD = (189, 138, 11)
        PLUM = (89, 6, 138)
        GREEN = (9, 112, 30)
        SCARLET = (255, 3, 7)
        PEACOCK = (20, 41, 156)

        self.window.fill(BACKGROUND)

        # How I want this to look:
        # Hallway tiles will have a black outline, but rooms and out of bounds will be full tile color
        # If there is an entrance it will have an outline of the room color and be the entrance color

        # Board squares
        for r in range(0, 25):
            for c in range(0, 24):
                space_id = (r * 24) + c

                # Out of bounds
                if self.board[space_id].get_room() == RoomType.OUT_OF_BOUNDS:
                    rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                    pygame.draw.rect(self.window, OOB, rect)
                    self.board_mapping[space_id] = rect

                # Hallway
                elif self.board[space_id].get_room() == RoomType.HALLWAY:
                    rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                    pygame.draw.rect(self.window, OOB, rect)
                    entrance_rect = pygame.Rect((c * SQUARE_SIZE) + 1, (r * SQUARE_SIZE) + 1,
                                                SQUARE_SIZE - 2, SQUARE_SIZE - 2)
                    pygame.draw.rect(self.window, HALLWAY, entrance_rect)
                    self.board_mapping[space_id] = rect

                # Kitchen
                elif self.board[space_id].get_room() == RoomType.KITCHEN:
                    # Outline and different colors for entrances of a room
                    if space_id in self.entrances['Kitchen']:
                        rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        pygame.draw.rect(self.window, OOB, rect)
                        entrance_rect = pygame.Rect((c * SQUARE_SIZE) + 1, (r * SQUARE_SIZE) + 1,
                                                    SQUARE_SIZE - 2, SQUARE_SIZE - 2)
                        pygame.draw.rect(self.window, ENTRANCES, entrance_rect)
                        self.board_mapping[space_id] = rect

                    else:
                        rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        pygame.draw.rect(self.window, KITCHEN, rect)
                        self.board_mapping[space_id] = rect

                # Ballroom
                elif self.board[space_id].get_room() == RoomType.BALL:
                    # Outline and different colors for entrances of a room
                    if space_id in self.entrances['Ballroom']:
                        rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        pygame.draw.rect(self.window, OOB, rect)
                        entrance_rect = pygame.Rect((c * SQUARE_SIZE) + 1, (r * SQUARE_SIZE) + 1,
                                                    SQUARE_SIZE - 2, SQUARE_SIZE - 2)
                        pygame.draw.rect(self.window, ENTRANCES, entrance_rect)
                        self.board_mapping[space_id] = rect

                    else:
                        rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        pygame.draw.rect(self.window, BALL, rect)
                        self.board_mapping[space_id] = rect

                # Conservatory
                elif self.board[space_id].get_room() == RoomType.CONSERVATORY:
                    # Outline and different colors for entrances of a room
                    if space_id in self.entrances['Conservatory']:
                        rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        pygame.draw.rect(self.window, OOB, rect)
                        entrance_rect = pygame.Rect((c * SQUARE_SIZE) + 1, (r * SQUARE_SIZE) + 1,
                                                    SQUARE_SIZE - 2, SQUARE_SIZE - 2)
                        pygame.draw.rect(self.window, ENTRANCES, entrance_rect)
                        self.board_mapping[space_id] = rect

                    else:
                        rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        pygame.draw.rect(self.window, CONSERVATORY, rect)
                        self.board_mapping[space_id] = rect

                # Dining room
                elif self.board[space_id].get_room() == RoomType.DINING:
                    # Outline and different colors for entrances of a room
                    if space_id in self.entrances['Dining Room']:
                        rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        pygame.draw.rect(self.window, OOB, rect)
                        entrance_rect = pygame.Rect((c * SQUARE_SIZE) + 1, (r * SQUARE_SIZE) + 1,
                                                    SQUARE_SIZE - 2, SQUARE_SIZE - 2)
                        pygame.draw.rect(self.window, ENTRANCES, entrance_rect)
                        self.board_mapping[space_id] = rect

                    else:
                        rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        pygame.draw.rect(self.window, DINING, rect)
                        self.board_mapping[space_id] = rect

                # Lounge
                elif self.board[space_id].get_room() == RoomType.LOUNGE:
                    # Outline and different colors for entrances of a room
                    if space_id in self.entrances['Lounge']:
                        rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        pygame.draw.rect(self.window, OOB, rect)
                        entrance_rect = pygame.Rect((c * SQUARE_SIZE) + 1, (r * SQUARE_SIZE) + 1,
                                                    SQUARE_SIZE - 2, SQUARE_SIZE - 2)
                        pygame.draw.rect(self.window, ENTRANCES, entrance_rect)
                        self.board_mapping[space_id] = rect

                    else:
                        rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        pygame.draw.rect(self.window, LOUNGE, rect)
                        self.board_mapping[space_id] = rect

                # Library
                elif self.board[space_id].get_room() == RoomType.LIBRARY:
                    # Outline and different colors for entrances of a room
                    if space_id in self.entrances['Library']:
                        rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        pygame.draw.rect(self.window, OOB, rect)
                        entrance_rect = pygame.Rect((c * SQUARE_SIZE) + 1, (r * SQUARE_SIZE) + 1,
                                                    SQUARE_SIZE - 2, SQUARE_SIZE - 2)
                        pygame.draw.rect(self.window, ENTRANCES, entrance_rect)
                        self.board_mapping[space_id] = rect

                    else:
                        rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        pygame.draw.rect(self.window, LIBRARY, rect)
                        self.board_mapping[space_id] = rect

                # Study
                elif self.board[space_id].get_room() == RoomType.STUDY:
                    # Outline and different colors for entrances of a room
                    if space_id in self.entrances['Study']:
                        rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        pygame.draw.rect(self.window, OOB, rect)
                        entrance_rect = pygame.Rect((c * SQUARE_SIZE) + 1, (r * SQUARE_SIZE) + 1,
                                                    SQUARE_SIZE - 2, SQUARE_SIZE - 2)
                        pygame.draw.rect(self.window, ENTRANCES, entrance_rect)
                        self.board_mapping[space_id] = rect

                    else:
                        rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        pygame.draw.rect(self.window, STUDY, rect)
                        self.board_mapping[space_id] = rect

                # Hall
                elif self.board[space_id].get_room() == RoomType.HALL:
                    # Outline and different colors for entrances of a room
                    if space_id in self.entrances['Hall']:
                        rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        pygame.draw.rect(self.window, OOB, rect)
                        entrance_rect = pygame.Rect((c * SQUARE_SIZE) + 1, (r * SQUARE_SIZE) + 1,
                                                    SQUARE_SIZE - 2, SQUARE_SIZE - 2)
                        pygame.draw.rect(self.window, ENTRANCES, entrance_rect)
                        self.board_mapping[space_id] = rect

                    else:
                        rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        pygame.draw.rect(self.window, HALL, rect)
                        self.board_mapping[space_id] = rect

                # Billiard Room
                elif self.board[space_id].get_room() == RoomType.BILLIARD:
                    # Outline and different colors for entrances of a room
                    if space_id in self.entrances['Billiard Room']:
                        rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        pygame.draw.rect(self.window, OOB, rect)
                        entrance_rect = pygame.Rect((c * SQUARE_SIZE) + 1, (r * SQUARE_SIZE) + 1,
                                                    SQUARE_SIZE - 2, SQUARE_SIZE - 2)
                        pygame.draw.rect(self.window, ENTRANCES, entrance_rect)
                        self.board_mapping[space_id] = rect

                    else:
                        rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        pygame.draw.rect(self.window, BILLIARDS, rect)
                        self.board_mapping[space_id] = rect

                # Start positions
                else:
                    if constants.START_POSITIONS['Colonel Mustard'] == space_id:
                        color = MUSTARD
                    elif constants.START_POSITIONS['Miss Scarlet'] == space_id:
                        color = SCARLET
                    elif constants.START_POSITIONS['Mr.Peacock'] == space_id:
                        color = PEACOCK
                    elif constants.START_POSITIONS['Mrs.White'] == space_id:
                        color = WHITE
                    elif constants.START_POSITIONS['Professor Plum'] == space_id:
                        color = PLUM
                    else:
                        # Reverend Green
                        color = GREEN

                    rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                    pygame.draw.rect(self.window, OOB, rect)
                    entrance_rect = pygame.Rect((c * SQUARE_SIZE) + 1, (r * SQUARE_SIZE) + 1,
                                                SQUARE_SIZE - 2, SQUARE_SIZE - 2)
                    pygame.draw.rect(self.window, color, entrance_rect)
                    self.board_mapping[space_id] = rect

        # Outline of the board
        pygame.draw.line(self.window, OOB, (0, 0), (600, 0))
        pygame.draw.line(self.window, OOB, (600, 0), (600, 625))
        pygame.draw.line(self.window, OOB, (0, 625), (600, 625))
        pygame.draw.line(self.window, OOB, (0, 0), (0, 625))

        # Room labels
        font = pygame.font.SysFont('freesansbold.ttf', 22)
        self.window.blit(font.render('Ballroom', True, OOB), (275, 120))
        self.window.blit(font.render('Billiard room', True, OOB), (480, 257))
        self.window.blit(font.render('Conservatory', True, OOB), (475, 57))
        self.window.blit(font.render('Dining room', True, OOB), (50, 307))
        self.window.blit(font.render('Hall', True, OOB), (289, 507))
        self.window.blit(font.render('Kitchen', True, OOB), (50, 57))
        self.window.blit(font.render('Library', True, OOB), (495, 407))
        self.window.blit(font.render('Lounge', True, OOB), (50, 532))
        self.window.blit(font.render('Study', True, OOB), (495, 557))

        # Header label
        header = pygame.font.SysFont('freesansbold.ttf', 40)
        self.window.blit(header.render('CLUE', True, WHITE), (275, 325))

        # Spawn labels
        self.window.blit(font.render('W', True, OOB), (230, 7))
        self.window.blit(font.render('G', True, OOB), (357, 7))
        self.window.blit(font.render('PK', True, OOB), (577, 157))
        self.window.blit(font.render('M', True, OOB), (6, 432))
        self.window.blit(font.render('PL', True, OOB), (577, 482))
        self.window.blit(font.render('S', True, OOB), (182, 607))

    def get_mapping(self, key):
        if key in self.board_mapping:
            return self.board_mapping[key]

    def in_room(self, position):
        return self.board[position].get_room().value

    def refresh_room_occupied(self):
        self.room_occupied = {'Ballroom': [False, False, False, False, False, False],
                              'Billiard Room': [False, False, False, False, False, False],
                              'Conservatory': [False, False, False, False, False, False],
                              'Dining Room': [False, False, False, False, False, False],
                              'Hall': [False, False, False, False, False, False],
                              'Kitchen': [False, False, False, False, False, False],
                              'Library': [False, False, False, False, False, False],
                              'Lounge': [False, False, False, False, False, False],
                              'Study': [False, False, False, False, False, False]}
