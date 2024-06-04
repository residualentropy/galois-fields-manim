from manim import *

class WhyGalois(Scene):
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
        ### by doing a bunch of math
        
