
# 日本語

GAME言語からCへ変換するコンパイラをpythonで書いてみました。

GAME言語コンパイラ -  miep2.py

`./miep2.py file.gm >out.c`とすると、GAME言語で書かれたfile.gmをCのソースに変換し、out.cに出力します。

本当はMIEP2ではなく、MIEPにしたいのですが、MIEPという名前は、43年前に中学生の僕と師匠の浜田さんがMicro Integer Expression Processorとして、自作のゲーム言語互換インタプリタ・コンパイラシステムに既に名付けていたので、2が付きました。

out.cはccでコンパイル可能です。 `cc out.c -o a.out`、`./a.out`で実行することが出来ます。

一般に冗長さを許せば、低級なプログラム言語で書かれたソースは、より高級なプログラム言語に翻訳することが容易です。

最適化はできていません。エラーチェックが甘いです。

ccのインラインアセンブラを使用しているので、x86_64 linuxシステム用です。

!=n(gosub)と] (ret) が機械依存部で、それ以外は機械独立です。完全に機械独立にし、一般のCコンパイラに掛けることができるようにすることが今後の課題ですが、C言語の仕様上、サブルーチン呼び出しを記述するのは難しいかも知れません。

一応完成

version 1.0.0 2024/8/26

ちょっとヴァージョンアップ、改名。

version 1.0.1 2024/8/27

# 今後の課題の問題点

・for-next,do-untl文の、for文またはdo文一つに対して複数のnext文、until文がある場合には対応していません。

・for-next文の制御変数に配列が使えない

・for文の終値に変数を使うと、カウントアップとして扱われる。

・next文に２重以上の括弧があるとバグる。

# in English 

I wrote a compiler in python to convert from GAME language to C.

GAME language compiler - miep2.py

`. /miep2.py file.gm >out.c` will convert file.gm written in GAME language to C source and output to out.c.

Actually, I would like to name it MIEP instead of MIEP2, but the name MIEP was already given to my own game language compatible interpreter/compiler system as Micro Integer Expression Processor by me, a junior high school student, and my teacher, Mr. Hamada, 43 years ago, so it was named 2 was added.

out.c can be compiled with cc. `cc out.c -o a.out`, `. /a.out` to execute it.

In general, if verbosity is allowed, sources written in lower-level programming languages can be easily translated into higher-level programming languages.

It is not optimized. Error checking is lax.

It uses the cc inline assembler and is for x86_64 linux systems.

! =n(gosub) and] (ret) are machine dependent parts, the rest are machine independent. It is my future task to make it completely machine-independent so that it can be hung on a general C compiler, but it may be difficult to write subroutine calls due to the C language specification.

Any way completed.

version 1.0.0 8/26/2024

A little version up, renamed.

version 1.0.1 8/27/2024

# Issues for future work

The for-next and do-untl statements do not support the case where there are multiple next and until statements for a single for or do statement.

Arrays cannot be used as control variables in the for-next statement.

If a variable is used for the end value of a for statement, it is treated as a count-up.

If there are two or more parentheses in the next statement, it is buggy.

Translated with DeepL.com (free version)
