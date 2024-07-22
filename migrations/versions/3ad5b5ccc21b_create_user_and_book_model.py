"""create User and Book Model

Revision ID: 3ad5b5ccc21b
Revises: 
Create Date: 2024-07-23 00:33:47.755230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ad5b5ccc21b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('second_name', sa.String(length=50), nullable=False),
    sa.Column('avatar', sa.LargeBinary(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('book',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('page_count', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('genre',
    sa.Column('name', sa.Enum('Romance', 'Fantasy', 'Science Fiction', 'Mystery', 'Horror', name='genre_enum'), nullable=False),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('book_genre',
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('genre_name', sa.Enum('Romance', 'Fantasy', 'Science Fiction', 'Mystery', 'Horror', name='genre_enum'), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.ForeignKeyConstraint(['genre_name'], ['genre.name'], ),
    sa.PrimaryKeyConstraint('book_id', 'genre_name')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('book_genre')
    op.drop_table('genre')
    op.drop_table('book')
    op.drop_table('user')
    # ### end Alembic commands ###
