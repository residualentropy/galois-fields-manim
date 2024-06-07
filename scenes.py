from manim import *
from manim_slides.slide import Slide

class Top(Slide):
    def construct(self):
        self.the_basic_setup()
        self.why_not_integers()
        self.prime_fields()
        self.hierarchy()
        self.extension_fields()
        self.the_aes_field()

    def p(self, *args):
        sq = Square(0.1, color= "black").to_edge(LEFT)
        self.play(Create(sq, run_time= 0.2))
        self.play(*args)
        self.play(Uncreate(sq, run_time= 0.2))

    def the_basic_setup(self):
        ### The stuff we want to encrypt, usually called the "plaintext",
        ### and can represent almost anything,
        pt_txt = Tex(r"\texttt{ATTACK AT DAWN}", font_size= 80)
        self.p(Write(pt_txt))
        self.next_slide()
        ### but we generally represent it just as ones and zeroes.
        pt_bin = Tex(r"\texttt{10101100111101}", font_size= 80)
        self.p(Transform(pt_txt, pt_bin))
        self.next_slide()
        ### We can then encrypt it
        encrypt_arrow = Arrow(start= UP * 2, end= DOWN * 2, buff= MED_LARGE_BUFF)
        ct_bin = Tex(r"\texttt{01010011000010}", font_size= 80).shift(DOWN * 2)
        self.p(pt_txt.animate.shift(UP * 2))
        self.p(
            Write(encrypt_arrow),
            Write(ct_bin),
        )
        self.next_slide()
        ### by doing a bunch of math,
        mafs = MathTex(r'''\begin{matrix}
            + & - \\
            \times & \div
        \end{matrix}''', font_size= 80)
        self.p(Write(mafs))
        self.next_slide()
        ### But we can't do normal binary math
        weird = Tex(r"$\leftarrow$ Weird", font_size= 70, color= "yellow").shift(RIGHT * 3)
        self.p(Write(weird))
        self.next_slide()
        ### because binary numbers aren't finite
        finite = Tex(r"Must be \emph{finite}", font_size= 70, color= "yellow").shift(RIGHT * 4)
        self.p(Transform(weird, finite))
        self.next_slide()
        self.p(
            Unwrite(encrypt_arrow),
            Unwrite(ct_bin),
            Unwrite(pt_txt),
            Unwrite(mafs),
            Unwrite(weird),
        )

    def why_not_integers(self):
        ### If we add two 3-digit binary numbers
        addition = MathTex(r"111 + 111", font_size= 80)
        self.p(Write(addition))
        self.next_slide()
        ### we get a 4-digit number.
        addition_full = MathTex(r"111 + 111 = 1110", font_size= 80)
        self.p(Transform(addition, addition_full))
        self.next_slide()
        ### If we multiply them, we get a 6-digit number.
        mult = MathTex(r"111 \times 111 = 110001", font_size= 80).shift(DOWN)
        self.p(
            addition.animate.shift(UP),
            Write(mult),
        )
        self.next_slide()
        ### This occurs because what we actually have
        self.p(
            Unwrite(addition),
            Unwrite(mult),
        )
        ### are operations
        mafs = MathTex(r'''\begin{matrix}
            + & - \\
            \times & \div
        \end{matrix}''', font_size= 50).shift(2 * DOWN)
        self.p(Write(mafs))
        self.next_slide()
        ### which act on binary numbers
        binary = MathTex(r"\{0, 1, 10, 11, \cdots\}", font_size=80)
        self.p(Write(binary))
        self.next_slide()
        ### and the set of binary numbers
        self.p(mafs.animate.set_color('grey'))
        ### is infinite.
        infinite = MathTex(r"\infty", font_size=70, color= "yellow").shift(2 * UP)
        arrow = Arrow(start= infinite.get_bottom(), end= binary.get_top(), color="yellow")
        self.p(
            Write(infinite),
            Write(arrow),
        )
        self.next_slide()
        self.p(
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
        self.p(Write(table))
        self.next_slide()
        ### computers handle arbitrary-size numbers all the time.
        self.p(*(
            obj.animate.set_opacity(1) for grp in table.get_columns()[0] for obj in grp
        ))
        self.next_slide()
        ### We can't use them for encryption though, since their implementations leak how
        ### how big they are.
        disclaimer = Tex(
            "*according to sketchy Python I spent 30 seconds on",
            font_size=20,
        ).shift((3 * DOWN) + (3 * RIGHT))
        self.p(
            *(
                obj.animate.set_opacity(1) \
                    for col in table.get_columns()[1:] \
                        for grp in col \
                            for obj in grp
            ),
            Write(disclaimer),
        )
        self.next_slide()
        ### They would also be super slow,
        ### and proving they're secure would be much more difficult.
        self.p(
            Unwrite(table),
            Unwrite(disclaimer),
        )

    def prime_fields(self):
        ### The first trick we need is modulo arithmetic,
        ma = MathTex(r"3 + 3 = 6", font_size= 80)
        self.p(Write(ma))
        ### where numbers simply wrap around.
        ma_actual = MathTex(r"3 + 3 = 0\quad(\operatorname{mod} 6)", font_size= 80)
        self.p(Transform(ma, ma_actual))
        self.next_slide()
        ### You can pick a different "modulo" at which you jump
        ### back to zero.
        ma_alt = MathTex(r"3 + 3 = 2\quad(\operatorname{mod} 4)", font_size= 80)
        self.p(Transform(ma, ma_alt))
        self.next_slide()
        ### However, it turns out that in order to have division,
        division = MathTex(r"\div", font_size= 100, color= "red").shift(2 * DOWN)
        self.p(
            Write(division),
            Transform(ma, ma_alt.shift(UP)),
        )
        self.next_slide()
        ### the modulo must be prime.
        ma_prime = MathTex(r"3 + 3 = 1\quad(\operatorname{mod} 5)", font_size= 80).shift(UP)
        self.p(
            Transform(ma, ma_prime),
            division.animate.set_color("green"),
        )
        self.next_slide()
        ### But we now have definitions for the four basic operations,
        mafs = MathTex(r'''\begin{matrix}
            + & - \\
            \times & \div
        \end{matrix}''', font_size= 80).shift(2 * DOWN)
        self.p(Transform(division, mafs))
        self.next_slide()
        #### (which is just "do them modulo p")
        pf_mafs = MathTex(r'''\begin{matrix}
            + & - \\
            \times & \div
        \end{matrix}\quad(\operatorname{mod} p)''', font_size= 80).shift(2 * DOWN)
        self.p(Transform(division, pf_mafs))
        self.next_slide()
        ### for a finite set.
        pf_set = MathTex(r"\{0, 1, 2, \cdots, p - 1\}", font_size= 80).shift(UP)
        self.p(Transform(ma, pf_set))
        self.next_slide()
        ### Any set of mathematical objects
        fb = SurroundingRectangle(ma, buff= 0.1)
        self.p(Create(fb))
        self.next_slide()
        ### which we can add, subtract, multiply, and divide,
        fb_ops = SurroundingRectangle(division, buff= 0.1)
        self.p(Transform(fb, fb_ops))
        self.next_slide()
        ### is called a field.
        field_text = Tex(r"A \emph{Field}", font_size= 80).to_corner(UR)
        fb_field = SurroundingRectangle(VGroup(ma, division), buff= 0.1)
        self.p(
            Write(field_text),
            Transform(fb, fb_field),
        )
        ### This type of field is known as a prime field.
        self.next_slide()
        prime_field_text = Tex(r"A \emph{Prime Field}", font_size= 80).to_corner(UR)
        self.p(Transform(field_text, prime_field_text))
        ### Prime fields are one type of Galois field-
        self.next_slide()
        gf_text_text = Tex(r"A \emph{Galois Field}", font_size= 80).to_corner(UR)
        self.p(Transform(field_text, gf_text_text))
        ### the type with a prime number of elements.
        self.next_slide()
        gf_text = MathTex(r"\operatorname{GF}(p)", font_size= 80).to_corner(UR)
        self.p(Transform(field_text, gf_text))
        ### This isn't what we need to represent a sequence of bits, but it does
        ### let us represent just one.
        self.next_slide()
        gf2_text = MathTex(r"\operatorname{GF}(2)", font_size= 80).to_corner(UR)
        gf2_set = MathTex(r"\{0, 1\}", font_size= 80).shift(UP)
        gf2_mafs = MathTex(r'''\begin{matrix}
            + & - \\
            \times & \div
        \end{matrix}\quad(\operatorname{mod} 2)''', font_size= 80).shift(2 * DOWN)
        self.p(
            Transform(field_text, gf2_text),
            Transform(ma, gf2_set),
            Transform(division, gf2_mafs),
        )
        self.next_slide()
        self.p(
            Unwrite(field_text),
            Uncreate(fb),
            Unwrite(ma),
            Unwrite(division),
        )

    def hierarchy(self):
        fields = Tex(r"Fields", font_size= 80).shift(UP * 3)
        self.p(Write(fields))
        self.next_slide()
        integers = Tex(r"Integers", font_size= 80)
        fields_to_integers = Arrow(start= fields.get_bottom(), end= integers.get_top())
        self.p(
            Write(integers),
            Write(fields_to_integers),
        )
        self.next_slide()
        integers_symbol = MathTex(r"\mathbb{Z}", font_size= 80)
        self.p(Transform(integers, integers_symbol))
        self.next_slide()
        galois = Tex(r"Galois Fields", font_size= 80).shift(LEFT * 2)
        integers_shifted = integers_symbol.shift(RIGHT * 2)
        fields_to_integers_shifted = Arrow(
            start= fields.get_bottom(),
            end= integers_shifted.get_top(),
        )
        fields_to_galois = Arrow(start= fields.get_bottom(), end= galois.get_top())
        self.p(
            Write(galois),
            Write(fields_to_galois),
            Transform(integers, integers_shifted),
            Transform(fields_to_integers, fields_to_integers_shifted),
        )
        self.next_slide()
        pf = Tex(r"Prime Fields", font_size= 80).shift((3 * DOWN) + (2 * LEFT))
        galois_to_pf = Arrow(start= galois.get_bottom(), end= pf.get_top())
        self.p(
            Write(pf),
            Write(galois_to_pf),
        )
        self.next_slide()
        pf_symbol = MathTex(r"\operatorname{GF}(p)", font_size= 80).shift((3 * DOWN) + (2 * LEFT))
        self.p(Transform(pf, pf_symbol))
        self.next_slide()
        pf_shifted = pf_symbol.shift(2 * LEFT)
        galois_to_pf_shifted = Arrow(start= galois.get_bottom(), end= pf_shifted.get_top())
        ef = Tex("Extension Fields", font_size= 80).shift((3 * DOWN) + RIGHT)
        galois_to_ef = Arrow(start= galois.get_bottom(), end= ef.get_top())
        self.p(
            Transform(pf, pf_shifted),
            Transform(galois_to_pf, galois_to_pf_shifted),
        )
        self.p(
            Write(ef),
            Write(galois_to_ef),
        )
        self.next_slide()
        ef_color = Tex(r"Extension Fields", font_size= 80, color= 'green').shift((3 * DOWN) + RIGHT)
        self.p(Transform(ef, ef_color))
        self.next_slide()
        ef_symbol = MathTex(r"\operatorname{GF}(p^m)", font_size= 80, color= 'green').shift(3 * DOWN)
        galois_to_ef_symbol = Arrow(start= galois.get_bottom(), end= ef_symbol.get_top())
        self.p(
            Transform(ef, ef_symbol),
            Transform(galois_to_ef, galois_to_ef_symbol),
        )
        self.next_slide()
        self.p(
            Unwrite(fields),
            Unwrite(integers),
            Unwrite(fields_to_integers),
            Unwrite(galois),
            Unwrite(fields_to_galois),
            Unwrite(pf),
            Unwrite(galois_to_pf),
            Unwrite(ef),
            Unwrite(galois_to_ef),
        )

    def extension_fields(self):
        what = MathTex(r"\operatorname{GF}(p)", font_size= 80).to_corner(UR)
        objects = MathTex(r"\{0, 1, \cdots, p - 1\}", font_size= 80).shift(UP)
        self.p(
            Write(what),
            Write(objects),
        )
        self.next_slide()
        what_ef = MathTex(r"\operatorname{GF}(p^1)", font_size= 80).to_corner(UR)
        objects_ef_one = MathTex(r"a_0", font_size= 80).shift(UP)
        a0_in_gfp = MathTex(r"a_0 \in \operatorname{GF}(p)", font_size= 80).shift(DOWN)
        self.p(
            Transform(what, what_ef),
            Transform(objects, objects_ef_one),
            Write(a0_in_gfp),
        )
        self.next_slide()
        objects_ef_gfp3 = MathTex(r"a_2", r"x^2", r" + ", r"a_1", r"x", r" + ", r"a_0", font_size= 80) \
            .shift(UP).set_color_by_tex(r"x", "orange")
        what_ef_gfp3 = MathTex(r"\operatorname{GF}(p^3)", font_size= 80).to_corner(UR)
        ai_in_gfp = MathTex(r"a_i \in \operatorname{GF}(p)", font_size= 80).shift(DOWN)
        self.p(
            Transform(objects, objects_ef_gfp3),
            Transform(what, what_ef_gfp3),
            Transform(a0_in_gfp, ai_in_gfp),
        )
        self.next_slide()
        objects_ef_gfpm = MathTex(r"a_{m-1}", r"x^{m - 1}", r" + \cdots + ", r"a_1", r"x", r" + ", r"a_0", font_size= 80) \
            .shift(UP).set_color_by_tex(r"x", "orange")
        what_ef_gfpm = MathTex(r"\operatorname{GF}(p^m)", font_size= 80).to_corner(UR)
        self.p(
            Transform(objects, objects_ef_gfpm),
            Transform(what, what_ef_gfpm),
        )
        self.next_slide()
        the_problem = Tex(r"The Problem", font_size= 80, color= "red").to_corner(UL)
        self.p(
            Unwrite(objects),
            Unwrite(a0_in_gfp),
            Write(the_problem),
        )
        mult = MathTex(r"a \times b", font_size= 80)
        what_gf23 = MathTex(r"\operatorname{GF}(2^3)", font_size= 80).to_corner(UR)
        self.p(
            Write(mult),
            Transform(what, what_gf23),
        )
        self.next_slide()
        mult_exp = MathTex(r"x", r" \times ", r"x^2", font_size= 80).set_color_by_tex(r"x", "orange")
        self.p(Transform(mult, mult_exp))
        self.next_slide()
        mult_uh_oh = MathTex(r"x^3", font_size= 80, color= "red")
        self.p(Transform(mult, mult_uh_oh))
        self.next_slide()
        mult_fixie_wixied = MathTex(r"x^3\quad(\operatorname{mod}", r"P", r")", font_size= 80, color= "green")
        self.p(Transform(mult, mult_fixie_wixied))
        self.next_slide()
        the_division_strikes_back = MathTex(r"\div", font_size= 150, color= "red").shift((LEFT * 4) + (2 * DOWN))
        self.p(Write(the_division_strikes_back))
        self.next_slide()
        pp = Tex(r"Prime Polynomial", font_size= 80).shift(mult_fixie_wixied[1].get_center()).shift(2 * DOWN)
        pp_arrow = Arrow(start= pp.get_top(), end= mult_fixie_wixied[1].get_bottom())
        self.p(
            Write(pp),
            Write(pp_arrow),
            the_division_strikes_back.animate.set_color("green"),
        )
        self.next_slide()
        self.p(
            Unwrite(the_division_strikes_back),
            the_problem.animate.set_color("green"),
        )
        self.next_slide()
        not_actually_pp = Tex(r"Irreducible Polynomial", font_size= 80).shift(mult_fixie_wixied[1].get_center()) \
            .shift(2 * DOWN)
        self.p(Transform(pp, not_actually_pp))
        self.next_slide()
        self.p(
            Unwrite(mult),
            Unwrite(pp),
            Unwrite(pp_arrow),
            Unwrite(the_problem),
        )
        self.p(Transform(what, what_ef_gfpm))
        self.next_slide()
        where = MathTex(r'''\text{where}\,\begin{matrix}
            a_i \in \operatorname{GF}(p)
        \end{matrix}''', font_size= 60).to_corner(UL)
        self.p(
            Write(objects_ef_gfpm),
            Write(where),
        )
        self.next_slide()
        ef_mafs = MathTex(r'''\begin{matrix}
            + & -
        \end{matrix}''', font_size= 80).shift(2 * DOWN)
        self.p(Write(ef_mafs))
        self.next_slide()
        ef_mafs_actual = MathTex(r'''\begin{matrix}
            + & -\\
            \times & \div & & (\operatorname{mod} P)
        \end{matrix}''', font_size= 80).shift(2 * DOWN)
        self.p(Transform(ef_mafs, ef_mafs_actual))
        self.next_slide()
        where_both = MathTex(r'''\text{where}\ \begin{matrix}
            a_i \in \operatorname{GF}(p) \\
            P\ \text{irreducible}
        \end{matrix}''', font_size= 60).to_corner(UL)
        self.p(Transform(where, where_both))
        self.next_slide()
        fb_ef = SurroundingRectangle(VGroup(objects_ef_gfpm, ef_mafs), buff= 0.1)
        self.p(Create(fb_ef))
        a_galois_field = Tex(r"\underline{\emph{A Galois Field}}", font_size= 80).to_corner(UR)
        self.p(Transform(what, a_galois_field))
        self.next_slide()
        self.p(
            Unwrite(objects_ef_gfpm),
            Unwrite(ef_mafs),
            Unwrite(what),
            Unwrite(where),
            Uncreate(fb_ef),
        )
    
    def the_aes_field(self):
        aes_field = Tex(r"\emph{The AES Field:}", font_size= 80).to_corner(UL)
        self.p(Write(aes_field))
        self.next_slide()
        aes_field_params = MathTex(r"\operatorname{GF}(2^{128})", font_size= 80)
        self.p(Write(aes_field_params))
        self.next_slide()
        irr_polynomial = Tex(r"(An Irreducible Polynomial)", font_size= 80) \
            .shift(2 * DOWN)
        self.p(Write(irr_polynomial))
        self.next_slide()
        aes_irr_polynomial = MathTex(
            "x^8", "+", "x^4", "+", "x^3", "+", "x", "+", "1",
            font_size= 80,
        ) \
            .set_color_by_tex(r"x", "orange") \
            .set_color_by_tex(r"1", "orange") \
            .shift(2 * DOWN)
        self.p(Transform(irr_polynomial, aes_irr_polynomial))
        self.next_slide()
        self.p(
            Unwrite(aes_field),
            Unwrite(aes_field_params),
            Unwrite(irr_polynomial),
        )
