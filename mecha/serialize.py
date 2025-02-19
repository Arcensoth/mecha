__all__ = [
    "Serializer",
]


import json
import re
from dataclasses import dataclass, field
from typing import Any, Iterable, Iterator, List, Optional

from beet.core.utils import required_field

from .ast import (
    AstBlock,
    AstBlockState,
    AstBool,
    AstChildren,
    AstCommand,
    AstCoordinate,
    AstItem,
    AstJson,
    AstLiteral,
    AstMessage,
    AstNbt,
    AstNbtPath,
    AstNbtPathSubscript,
    AstNode,
    AstNumber,
    AstParticle,
    AstParticleParameters,
    AstRange,
    AstResourceLocation,
    AstRoot,
    AstSelector,
    AstSelectorAdvancementMatch,
    AstSelectorAdvancementPredicateMatch,
    AstSelectorAdvancements,
    AstSelectorArgument,
    AstSelectorScoreMatch,
    AstSelectorScores,
    AstString,
    AstTime,
    AstUUID,
    AstVector2,
    AstVector3,
)
from .database import CompilationDatabase
from .dispatch import Visitor, rule
from .spec import CommandSpec
from .utils import QuoteHelper, number_to_string

REGEX_COMMENTS = re.compile(r"^(?:(\s*#.*)|.+)", re.MULTILINE)


@dataclass
class Serializer(Visitor):
    spec: CommandSpec = required_field()
    database: CompilationDatabase = field(default_factory=CompilationDatabase)

    keep_comments: bool = False

    regex_comments: "re.Pattern[str]" = field(default=REGEX_COMMENTS)
    quote_helper: QuoteHelper = field(
        default_factory=lambda: QuoteHelper(
            escape_sequences={
                r"\\": "\\",
                r"\f": "\f",
                r"\n": "\n",
                r"\r": "\r",
                r"\t": "\t",
            }
        )
    )

    def __call__(self, node: AstNode, keep_comments: Optional[bool] = None) -> str:
        result: List[str] = []

        if keep_comments is not None:
            self.keep_comments, keep_comments = keep_comments, self.keep_comments

        try:
            self.invoke(node, result)
        finally:
            if keep_comments is not None:
                self.keep_comments = keep_comments

        return "".join(result)

    def collection(
        self,
        nodes: Iterable[AstNode],
        delimitters: str,
        result: List[str],
    ) -> Iterator[AstNode]:
        """Helper for serializing collections."""
        result.append(delimitters[0])
        sep = ""
        for node in nodes:
            result.append(sep)
            sep = ", "
            yield node
        result.append(delimitters[-1])

    def key_value(self, node: Any, sep: str, result: List[str]) -> Iterator[AstNode]:
        """Helper for serializing key-value pairs."""
        yield node.key
        result.append(sep)
        yield node.value

    @rule(AstNode)
    def unserializable(self, node: AstNode, result: List[str]):
        raise ValueError(f"Couldn't serialize {type(node)!r} node.")

    @rule(AstVector2)
    @rule(AstVector3)
    @rule(AstParticleParameters)
    @rule(AstParticle)
    def aggregate(self, node: AstNode, result: List[str]):
        sep = ""
        for child in node:
            result.append(sep)
            sep = " "
            yield child

    @rule(AstRoot)
    def root(self, node: AstRoot, result: List[str]):
        pos = 0
        source = self.keep_comments and self.database[self.database.current].source

        for command in node.commands:
            if source:
                end_pos = max(command.location.pos, pos + 1)
                if pos > -1:
                    if fill := source[pos:end_pos]:
                        result.append(self.regex_comments.sub(r"\1", fill))
                try:
                    pos = source.index("\n", end_pos) + 1
                except ValueError:
                    pos = -1

            yield command
            result.append("\n")

        if source and pos > -1:
            if fill := source[pos:]:
                result.append(self.regex_comments.sub(r"\1", fill))

    @rule(AstCommand)
    def command(self, node: AstCommand, result: List[str]):
        prototype = self.spec.prototypes[node.identifier]
        argument_index = 0

        sep = ""
        for token in prototype.signature:
            result.append(sep)
            sep = " "

            if isinstance(token, str):
                result.append(token)
            else:
                yield node.arguments[argument_index]
                argument_index += 1

    @rule(AstLiteral)
    def literal(self, node: AstLiteral, result: List[str]):
        result.append(node.value)

    @rule(AstString)
    def string(self, node: AstString, result: List[str]):
        result.append(self.quote_helper.quote_string(node.value))

    @rule(AstBool)
    def bool(self, node: AstBool, result: List[str]):
        result.append(str(node.value).lower())

    @rule(AstNumber)
    def number(self, node: AstNumber, result: List[str]):
        result.append(number_to_string(node.value))

    @rule(AstUUID)
    def uuid(self, node: AstUUID, result: List[str]):
        result.append(str(node.value))

    @rule(AstCoordinate)
    def coordinate(self, node: AstCoordinate, result: List[str]):
        if node.type == "relative":
            result.append("~")
            if node.value == 0:
                return
        elif node.type == "local":
            result.append("^")
            if node.value == 0:
                return
        result.append(number_to_string(node.value))

    @rule(AstJson)
    def json(self, node: AstJson, result: List[str]):
        result.append(json.dumps(node.evaluate()))

    @rule(AstNbt)
    def nbt(self, node: AstNbt, result: List[str]):
        result.append(node.evaluate().snbt())

    @rule(AstResourceLocation)
    def resource_location(self, node: AstResourceLocation, result: List[str]):
        result.append(node.get_value())

    @rule(AstBlockState)
    def block_state(self, node: AstBlockState, result: List[str]):
        yield from self.key_value(node, "=", result)

    @rule(AstBlock)
    def block(self, node: AstBlock, result: List[str]):
        yield node.identifier
        if node.block_states:
            yield from self.collection(node.block_states, "[]", result)
        if node.data_tags:
            yield node.data_tags

    @rule(AstItem)
    def item(self, node: AstItem, result: List[str]):
        yield node.identifier
        if node.data_tags:
            yield node.data_tags

    @rule(AstRange)
    def range(self, node: AstRange, result: List[str]):
        if node.exact:
            result.append(number_to_string(node.value))
        else:
            if node.min is not None:
                result.append(number_to_string(node.min))
            result.append("..")
            if node.max is not None:
                result.append(number_to_string(node.max))

    @rule(AstTime)
    def time(self, node: AstTime, result: List[str]):
        result.append(number_to_string(node.value))

        if node.unit == "day":
            result.append("d")
        elif node.unit == "second":
            result.append("s")

    @rule(AstSelectorScoreMatch)
    @rule(AstSelectorAdvancementPredicateMatch)
    def selector_argument_key_value(self, node: AstNode, result: List[str]):
        yield from self.key_value(node, "=", result)

    @rule(AstSelectorScores)
    def selector_scores(self, node: AstSelectorScores, result: List[str]):
        yield from self.collection(node.scores, "{}", result)

    @rule(AstSelectorAdvancementMatch)
    def selector_advancement_match(
        self,
        node: AstSelectorAdvancementMatch,
        result: List[str],
    ):
        yield node.key
        result.append("=")
        if isinstance(node.value, AstChildren):
            yield from self.collection(node.value, "{}", result)
        else:
            yield node.value

    @rule(AstSelectorAdvancements)
    def selector_advancements(self, node: AstSelectorAdvancements, result: List[str]):
        yield from self.collection(node.advancements, "{}", result)

    @rule(AstSelectorArgument)
    def selector_argument(self, node: AstSelectorArgument, result: List[str]):
        yield node.key
        result.append("=")
        if node.inverted:
            result.append("!")
        if node.value:
            yield node.value

    @rule(AstSelector)
    def selector(self, node: AstSelector, result: List[str]):
        result.append("@")
        result.append(node.variable)
        if node.arguments:
            yield from self.collection(node.arguments, "[]", result)

    @rule(AstMessage)
    def message(self, node: AstMessage, result: List[str]):
        yield from node.fragments

    @rule(AstNbtPathSubscript)
    def nbt_path_subscript(self, node: AstNbtPathSubscript, result: List[str]):
        result.append("[")
        if node.index:
            yield node.index
        result.append("]")

    @rule(AstNbtPath)
    def nbt_path(self, node: AstNbtPath, result: List[str]):
        sep = ""
        for component in node.components:
            if isinstance(component, AstString):
                result.append(sep)
            sep = "."
            yield component
