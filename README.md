# 日本語

GAME言語からCへ変換するコンパイラをpythonで書いてみました。

GAME言語コンパイラ -  miep2.py

`./miep2.py file.gm >out.c`とすると、GAME言語で書かれたfile.gmをCのソースファイルに変換し、out.cに出力します。

本当はMIEP2ではなく、MIEPにしたいのですが、MIEPという名前は、43年前にすでに中学生の僕と師匠の浜田さんがMicro Integer Expression Processorとして、自作のゲーム言語互換インタプリタ・コンパイラシステムに名付けていたので、2が付きました。

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

# in English

I wrote a compiler in python to convert from GAME language to C.

GAME language compiler - miep.py

. /miep2.py file.gm >out.c will convert file.gm written in GAME language to C source file and output to out.c.

I really want to use MIEP instead of MIEP2, but the name MIEP was already given 43 years ago by me, a junior high school student, and my teacher, Mr. Hamada, as Micro Integer Expression Processor, to a game language compatible interpreter/compiler system of our own making, 2 was attached.

out.c can be compiled with cc. cc out.c -o a.out, . /a.out can be used to execute it.

In general, if verbosity is allowed, sources written in lower-level programming languages are easier to translate into higher-level programming languages.

Optimization is not done. Error checking is lax.

It uses the cc inline assembler and is for x86_64 linux systems.

! =n(gosub) and] (ret) are machine dependent parts, the rest are machine independent. It is my future task to make it completely machine-independent so that it can be hung on a general C compiler, but it may be difficult to write subroutine calls due to the C language specification.

Completed

version 1.0.0 8/26/2024

A little version up, renamed.

version 1.0.1 8/27/2024

Problems for future issues
The for-next and do-untl statements do not support the case where there are multiple next and until statements for a single for or do statement.

Arrays cannot be used as control variables for for-next statements.

Translated with DeepL.com (free version)
