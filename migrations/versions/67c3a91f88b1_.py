"""empty message

Revision ID: 67c3a91f88b1
Revises: 
Create Date: 2019-06-22 09:17:14.628425

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67c3a91f88b1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book',
    sa.Column('b_id', sa.Integer(), nullable=False),
    sa.Column('b_name', sa.String(length=255), nullable=True),
    sa.Column('b_introduction', sa.String(length=1000), nullable=True),
    sa.Column('b_pulishing_house', sa.String(length=500), nullable=True),
    sa.Column('b_writer', sa.String(length=100), nullable=True),
    sa.Column('b_writer_intro', sa.String(length=1000), nullable=True),
    sa.Column('b_score', sa.Integer(), nullable=True),
    sa.Column('b_heat', sa.Integer(), nullable=True),
    sa.Column('b_date', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('b_id')
    )
    op.create_index(op.f('ix_book_b_name'), 'book', ['b_name'], unique=False)
    op.create_table('movie',
    sa.Column('mo_id', sa.Integer(), nullable=False),
    sa.Column('mo_English_name', sa.String(length=225), nullable=True),
    sa.Column('mo_name', sa.String(length=255), nullable=True),
    sa.Column('mo_introduction', sa.String(length=1000), nullable=True),
    sa.Column('mo_nation', sa.String(length=40), nullable=True),
    sa.Column('mo_heat', sa.Integer(), nullable=True),
    sa.Column('mo_picture', sa.String(length=5000), nullable=True),
    sa.Column('mo_length', sa.String(length=100), nullable=True),
    sa.Column('mo_score', sa.Integer(), nullable=True),
    sa.Column('mo_date', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('mo_id')
    )
    op.create_index(op.f('ix_movie_mo_English_name'), 'movie', ['mo_English_name'], unique=False)
    op.create_index(op.f('ix_movie_mo_name'), 'movie', ['mo_name'], unique=False)
    op.create_table('music',
    sa.Column('mu_id', sa.Integer(), nullable=False),
    sa.Column('mu_name', sa.String(length=255), nullable=True),
    sa.Column('mu_introduction', sa.String(length=1000), nullable=True),
    sa.Column('mu_singer', sa.String(length=100), nullable=True),
    sa.Column('mu_heat', sa.Integer(), nullable=True),
    sa.Column('mu_picture', sa.String(length=5000), nullable=True),
    sa.Column('mu_score', sa.Integer(), nullable=True),
    sa.Column('mu_date', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('mu_id')
    )
    op.create_index(op.f('ix_music_mu_name'), 'music', ['mu_name'], unique=False)
    op.create_table('tag',
    sa.Column('t_id', sa.Integer(), nullable=False),
    sa.Column('t_tag', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('t_id')
    )
    op.create_table('user',
    sa.Column('u_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('u_id')
    )
    op.create_table('TagToBook',
    sa.Column('t_id', sa.Integer(), nullable=True),
    sa.Column('b_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['b_id'], ['book.b_id'], ),
    sa.ForeignKeyConstraint(['t_id'], ['tag.t_id'], )
    )
    op.create_table('TagToMovie',
    sa.Column('t_id', sa.Integer(), nullable=True),
    sa.Column('mo_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['mo_id'], ['movie.mo_id'], ),
    sa.ForeignKeyConstraint(['t_id'], ['tag.t_id'], )
    )
    op.create_table('TagToMusic',
    sa.Column('t_id', sa.Integer(), nullable=True),
    sa.Column('mu_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['mu_id'], ['music.mu_id'], ),
    sa.ForeignKeyConstraint(['t_id'], ['tag.t_id'], )
    )
    op.create_table('UserLikeTags',
    sa.Column('t_id', sa.Integer(), nullable=True),
    sa.Column('u_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['t_id'], ['tag.t_id'], ),
    sa.ForeignKeyConstraint(['u_id'], ['user.u_id'], )
    )
    op.create_table('commentbook',
    sa.Column('com_user', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('com_book', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('comment', sa.String(length=1000), nullable=True),
    sa.Column('date', sa.DATETIME(), server_default=sa.text('NOW()'), nullable=False),
    sa.Column('score', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['com_book'], ['book.b_id'], ),
    sa.ForeignKeyConstraint(['com_user'], ['user.u_id'], ),
    sa.PrimaryKeyConstraint('com_user', 'com_book')
    )
    op.create_table('commentmovie',
    sa.Column('com_user', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('com_movie', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('comment', sa.String(length=1000), nullable=True),
    sa.Column('date', sa.DATETIME(), server_default=sa.text('NOW()'), nullable=False),
    sa.Column('score', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['com_movie'], ['movie.mo_id'], ),
    sa.ForeignKeyConstraint(['com_user'], ['user.u_id'], ),
    sa.PrimaryKeyConstraint('com_user', 'com_movie')
    )
    op.create_table('commentmusic',
    sa.Column('com_user', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('com_music', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('comment', sa.String(length=1000), nullable=True),
    sa.Column('date', sa.DATETIME(), server_default=sa.text('NOW()'), nullable=False),
    sa.Column('score', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['com_music'], ['music.mu_id'], ),
    sa.ForeignKeyConstraint(['com_user'], ['user.u_id'], ),
    sa.PrimaryKeyConstraint('com_user', 'com_music')
    )
    op.create_table('markbook',
    sa.Column('mark_user', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('mark_book', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('want_date', sa.DATETIME(), nullable=True),
    sa.Column('seen_date', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['mark_book'], ['book.b_id'], ),
    sa.ForeignKeyConstraint(['mark_user'], ['user.u_id'], ),
    sa.PrimaryKeyConstraint('mark_user', 'mark_book')
    )
    op.create_table('markmovie',
    sa.Column('mark_user', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('mark_movie', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('want_date', sa.DATETIME(), nullable=True),
    sa.Column('seen_date', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['mark_movie'], ['movie.mo_id'], ),
    sa.ForeignKeyConstraint(['mark_user'], ['user.u_id'], ),
    sa.PrimaryKeyConstraint('mark_user', 'mark_movie')
    )
    op.create_table('markmusic',
    sa.Column('mark_user', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('mark_music', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('want_date', sa.DATETIME(), nullable=True),
    sa.Column('seen_date', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['mark_music'], ['music.mu_id'], ),
    sa.ForeignKeyConstraint(['mark_user'], ['user.u_id'], ),
    sa.PrimaryKeyConstraint('mark_user', 'mark_music')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('markmusic')
    op.drop_table('markmovie')
    op.drop_table('markbook')
    op.drop_table('commentmusic')
    op.drop_table('commentmovie')
    op.drop_table('commentbook')
    op.drop_table('UserLikeTags')
    op.drop_table('TagToMusic')
    op.drop_table('TagToMovie')
    op.drop_table('TagToBook')
    op.drop_table('user')
    op.drop_table('tag')
    op.drop_index(op.f('ix_music_mu_name'), table_name='music')
    op.drop_table('music')
    op.drop_index(op.f('ix_movie_mo_name'), table_name='movie')
    op.drop_index(op.f('ix_movie_mo_English_name'), table_name='movie')
    op.drop_table('movie')
    op.drop_index(op.f('ix_book_b_name'), table_name='book')
    op.drop_table('book')
    # ### end Alembic commands ###
