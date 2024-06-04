from manim import *

class TheBasicSetup(Scene):
    def construct(self):
        ### The stuff we want to encrypt, usually called the "plaintext",
        ### and can represent almost anything,
        pt_txt = Tex(r"\texttt{ATTACK AT DAWN}", font_size= 80)
        self.play(Write(pt_txt))
        self.wait()
        ### but we generally represent it just as ones and zeroes.
        pt_bin = Tex(r"\texttt{10101100111101}", font_size= 80)
        self.play(Transform(pt_txt, pt_bin))
        self.wait()
        ### We can then encrypt it
        encrypt_arrow = Arrow(start= UP * 2, end= DOWN * 2, buff= MED_LARGE_BUFF)
        ct_bin = Tex(r"\texttt{01010011000010}", font_size= 80).shift(DOWN * 2)
        self.play(pt_txt.animate.shift(UP * 2))
        self.play(
            Write(encrypt_arrow),
            Write(ct_bin),
        )
        ### by doing a bunch of math,
        mafs = MathTex(r'''\begin{matrix}
            + & - \\
            \times & \div
        \end{matrix}''', font_size= 80)
        self.play(Write(mafs))
        ### But we can't do normal binary math
        weird = Tex(r"$\leftarrow$ Weird", font_size= 70, color= "yellow").shift(RIGHT * 3)
        self.play(Write(weird))
        ### because binary numbers aren't finite
        finite = Tex(r"Must be \emph{finite}", font_size= 70, color= "yellow").shift(RIGHT * 4)
        self.play(Transform(weird, finite))
        self.wait()
        self.play(
            Unwrite(encrypt_arrow),
            Unwrite(ct_bin),
            Unwrite(mafs),
            Unwrite(weird),
        )

class WhyGalois(Scene):
    def construct(self):
        ### If we add two 3-digit binary numbers
        addition = MathTex(r"111 + 111", font_size= 80)
        self.play(Write(addition))
        ### we get a 4-digit number.
        addition_full = MathTex(r"111 + 111 = 1110", font_size= 80)
        self.play(Transform(addition, addition_full))
        self.wait()
        ### If we multiply them, we get a 6-digit number.
        mult = MathTex(r"111 \times 111 = 110001", font_size= 80).shift(DOWN)
        self.play(
            addition.animate.shift(UP),
            Write(mult),
        )
        self.wait()
        ### This occurs because what we actually have
        self.play(
            Unwrite(addition),
            Unwrite(mult),
        )
        ### are operations
        mafs = MathTex(r'''\begin{matrix}
            + & - \\
            \times & \div
        \end{matrix}''', font_size= 50).shift(2 * DOWN)
        self.play(Write(mafs))
        ### which act on binary numbers
        binary = MathTex(r"\{0, 1, 10, 11, \cdots\}", font_size=80)
        self.play(Write(binary))
        ### and the set of binary numbers
        self.play(mafs.animate.set_color('grey'))
        ### is infinite.
        infinite = MathTex(r"\infty", font_size=70, color= "yellow").shift(2 * UP)
        arrow = Arrow(start= infinite.get_bottom(), end= binary.get_top(), color="yellow")
        self.play(
            Write(infinite),
            Write(arrow),
        )
        self.wait()
        self.play(
            Unwrite(infinite),
            Unwrite(arrow),
            Unwrite(binary),
            Unwrite(mafs),
        )
        ### You might think that this isn't a problem since
        table = Table([[
            "42", "1", "44.1",
        ], [
            "69,000,000", "4", "80.6",
        ]], col_labels= [
            Tex(""), mem_a := Tex("Min. size (Bytes)"), time_a := Tex(r"Time* of $n \times n$ (ns)"),
        ])
        for col in table.get_columns():
            for grp in col:
                for obj in grp:
                    obj.set_opacity(0)
        self.play(Write(table))
        ### computers handle arbitrary-size numbers all the time.
        self.play(*(
            obj.animate.set_opacity(1) for grp in table.get_columns()[0] for obj in grp
        ))
        ### We can't use them for encryption though, since their implementations leak how
        ### how big they are.
        disclaimer = Tex(
            "*according to sketchy Python I spent 30 seconds on",
            font_size=20,
        ).shift((3 * DOWN) + (3 * RIGHT))
        self.play(
            *(
                obj.animate.set_opacity(1) \
                    for col in table.get_columns()[1:] \
                        for grp in col \
                            for obj in grp
            ),
            Write(disclaimer),
        )
        ### They would also be super slow,
        self.wait()
        ### and proving they're secure would be much more difficult.
        self.play(
            Unwrite(table),
            Unwrite(disclaimer),
        )
        ### The first trick we need is modulo arithmetic,
        ma = MathTex(r"3 + 3 = 6", font_size= 80)
        self.play(Write(ma))
        ### where numbers simply wrap around.
        ma_actual = MathTex(r"3 + 3 = 0\quad(\operatorname{mod} 6)", font_size= 80)
        self.play(Transform(ma, ma_actual))
        self.wait()
        ### You can pick a different "modulo" at which you jump
        ### back to zero.
        ma_alt = MathTex(r"3 + 3 = 2\quad(\operatorname{mod} 4)", font_size= 80)
        self.play(Transform(ma, ma_alt))
        self.wait()
        ### However, it turns out that in order to have division,
        division = MathTex(r"\div", font_size= 100).shift(3 * DOWN)
        self.play(Write(division))
        ### the modulo must be prime.
        ma_prime = MathTex(r"3 + 3 = 1\quad(\operatorname{mod} 5)", font_size= 80)
        self.play(Transform(ma, ma_prime))
        self.wait()
