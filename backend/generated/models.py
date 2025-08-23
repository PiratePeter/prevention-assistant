from typing import Optional
import datetime

from sqlalchemy import DateTime, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class PreventionCase(Base):
    __tablename__ = 'prevention_case'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='prevention_case_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    creation_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    title: Mapped[Optional[str]] = mapped_column(Text)
    damage_desc: Mapped[Optional[str]] = mapped_column(Text)
    facade: Mapped[Optional[str]] = mapped_column(Text)
    basement: Mapped[Optional[str]] = mapped_column(Text)
    roof: Mapped[Optional[str]] = mapped_column(Text)
    heating: Mapped[Optional[str]] = mapped_column(Text)
    firstname: Mapped[Optional[str]] = mapped_column(Text)
    lastname: Mapped[Optional[str]] = mapped_column(Text)
    email: Mapped[Optional[str]] = mapped_column(Text)
    preventions: Mapped[Optional[str]] = mapped_column(Text)

    prevention_question: Mapped[list['PreventionQuestion']] = relationship('PreventionQuestion', back_populates='prevention_case')


class PreventionQuestion(Base):
    __tablename__ = 'prevention_question'
    __table_args__ = (
        ForeignKeyConstraint(['prevention_case_id'], ['prevention_case.id'], ondelete='CASCADE', name='fk_prevention_case'),
        PrimaryKeyConstraint('id', name='prevention_question_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prevention_case_id: Mapped[Optional[int]] = mapped_column(Integer)
    question_text: Mapped[Optional[str]] = mapped_column(Text)
    answer_text: Mapped[Optional[str]] = mapped_column(Text)

    prevention_case: Mapped[Optional['PreventionCase']] = relationship('PreventionCase', back_populates='prevention_question')
